import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { listSchemes, matchSchemes } from '../api/client';

const GovernmentSchemes: React.FC = () => {
  const { t, lang } = useLanguage();
  const [schemes, setSchemes] = useState<any[]>([]);
  const [matched, setMatched] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [matchCategory, setMatchCategory] = useState('dairy');
  const [matchDistrict, setMatchDistrict] = useState('Ahmednagar');
  const [matching, setMatching] = useState(false);

  useEffect(() => {
    listSchemes().then((res) => { setSchemes(res.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const getName = (s: any) => {
    if (lang === 'hi' && s.name_hi) return s.name_hi;
    if (lang === 'mr' && s.name_mr) return s.name_mr;
    return s.name;
  };
  const getDesc = (s: any) => {
    if (lang === 'hi' && s.description_hi) return s.description_hi;
    if (lang === 'mr' && s.description_mr) return s.description_mr;
    return s.description;
  };

  const handleMatch = async () => {
    setMatching(true);
    try {
      const res = await matchSchemes({ business_category: matchCategory, district: matchDistrict });
      setMatched(res.data);
    } catch (err: any) {
      alert('Matching failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setMatching(false);
    }
  };

  if (loading) return <div className="gu-spinner" />;

  return (
    <div>
      <h1 className="page-title">🏛️ {t('schemes')}</h1>

      {/* Matching Tool */}
      <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ margin: '0 0 1rem' }}>🔍 Find Matching Schemes</h3>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'end', flexWrap: 'wrap' }}>
          <div>
            <label className="gu-label">Business Category</label>
            <select className="gu-select" value={matchCategory} onChange={(e) => setMatchCategory(e.target.value)}>
              <option value="dairy">Dairy</option>
              <option value="livestock">Livestock / Goat</option>
              <option value="poultry">Poultry</option>
              <option value="food_processing">Food Processing</option>
              <option value="organic">Organic / Vermicompost</option>
              <option value="beekeeping">Beekeeping</option>
              <option value="retail">Retail / Agri-Input</option>
            </select>
          </div>
          <div>
            <label className="gu-label">{t('district')}</label>
            <select className="gu-select" value={matchDistrict} onChange={(e) => setMatchDistrict(e.target.value)}>
              <option value="Ahmednagar">Ahmednagar</option>
              <option value="Pune">Pune</option>
              <option value="Nashik">Nashik</option>
            </select>
          </div>
          <button className="gu-btn gu-btn-primary" onClick={handleMatch} disabled={matching}>
            {matching ? '⏳ Matching...' : '🔍 Match Schemes'}
          </button>
        </div>

        {matched && (
          <div style={{ marginTop: '1rem', padding: '1rem', background: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
            <strong>✅ {matched.matched_schemes?.length || 0} scheme(s) matched</strong>
            {matched.total_potential_support > 0 && (
              <span style={{ marginLeft: '1rem' }}>
                Total potential support: <strong>₹{matched.total_potential_support.toLocaleString()}</strong>
              </span>
            )}
            <p style={{ margin: '0.5rem 0 0', fontSize: '0.85rem', color: 'var(--gu-text-secondary)' }}>
              {matched.recommendation}
            </p>
          </div>
        )}
      </div>

      {/* Scheme Cards */}
      <div className="gu-badge gu-badge-demo" style={{ marginBottom: '1rem' }}>
        ⚠️ Demo/illustrative scheme records — verify with official sources
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '1rem' }}>
        {(matched?.matched_schemes || schemes).map((s: any) => {
          const isMatched = matched?.matched_schemes?.some((ms: any) => ms.id === s.id);
          return (
            <div
              key={s.id}
              className="gu-card"
              style={{
                border: isMatched ? '2px solid var(--gu-success)' : undefined,
                background: isMatched ? '#fefce8' : undefined,
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                <h3 style={{ margin: 0, fontSize: '1rem' }}>{getName(s)}</h3>
                <span className={`gu-badge ${s.scheme_type === 'Central' ? 'gu-badge-info' : 'gu-badge-medium'}`}>
                  {s.scheme_type}
                </span>
              </div>

              <p style={{ fontSize: '0.85rem', color: 'var(--gu-text-secondary)', margin: '0 0 1rem', lineHeight: 1.5 }}>
                {getDesc(s)}
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.85rem', marginBottom: '0.75rem' }}>
                <div>
                  <span style={{ color: 'var(--gu-text-secondary)' }}>{t('maxSupport')}:</span>
                  <div style={{ fontWeight: 700, color: 'var(--gu-success)' }}>
                    ₹{s.max_support?.toLocaleString() || 'Varies'}
                  </div>
                </div>
                <div>
                  <span style={{ color: 'var(--gu-text-secondary)' }}>Support Type:</span>
                  <div style={{ fontWeight: 600 }}>{s.support_type}</div>
                </div>
                {s.subsidy_percentage > 0 && (
                  <div>
                    <span style={{ color: 'var(--gu-text-secondary)' }}>Subsidy:</span>
                    <div style={{ fontWeight: 600 }}>{s.subsidy_percentage}%</div>
                  </div>
                )}
                <div>
                  <span style={{ color: 'var(--gu-text-secondary)' }}>Department:</span>
                  <div style={{ fontWeight: 500, fontSize: '0.8rem' }}>{s.department}</div>
                </div>
              </div>

              {s.eligibility_criteria && (
                <div style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px', fontSize: '0.8rem', marginBottom: '0.5rem' }}>
                  <strong>{t('eligibility')}:</strong> {s.eligibility_criteria}
                </div>
              )}

              {s.required_documents?.length > 0 && (
                <div style={{ fontSize: '0.8rem' }}>
                  <strong>{t('documents')}:</strong>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', marginTop: '0.25rem' }}>
                    {s.required_documents.map((doc: string) => (
                      <span key={doc} className="gu-badge" style={{ background: '#f1f5f9', color: '#475569' }}>{doc}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default GovernmentSchemes;
