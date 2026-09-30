import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { analyzeFeasibility, getProfile, getUserAssessments } from '../api/client';
import ScoreRing from '../components/ScoreRing';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

const FeasibilityAnalysis: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [profile, setProfile] = useState<any>(null);
  const [results, setResults] = useState<any[]>([]);
  const [assessments, setAssessments] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedRec, setSelectedRec] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const pRes = await getProfile();
        setProfile(pRes.data);
        const aRes = await getUserAssessments(user!.id);
        setAssessments(aRes.data);
      } catch {}
    };
    load();
  }, []);

  const runAnalysis = async () => {
    if (!profile) {
      setError('Please create your profile first before running the analysis.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await analyzeFeasibility({
        user_id: user!.id,
        district: profile.district,
      });
      setResults(res.data.recommendations);
      if (res.data.recommendations.length > 0) {
        setSelectedRec(res.data.recommendations[0]);
      }
      // Refresh assessments
      const aRes = await getUserAssessments(user!.id);
      setAssessments(aRes.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  const radarData = selectedRec ? [
    { factor: 'Capital Fit', score: selectedRec.capital_fit_score },
    { factor: 'Demand', score: selectedRec.demand_score },
    { factor: 'Competition', score: selectedRec.competition_score },
    { factor: 'Profit', score: selectedRec.profit_score },
    { factor: 'Skill Fit', score: selectedRec.skill_fit_score },
    { factor: 'Seasonality', score: selectedRec.seasonality_score },
    { factor: 'Infrastructure', score: selectedRec.infrastructure_score },
  ] : [];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 className="page-title" style={{ margin: 0 }}>📈 {t('feasibility')}</h1>
        <button className="gu-btn gu-btn-primary gu-btn-lg" onClick={runAnalysis} disabled={loading}>
          {loading ? '⏳ Analyzing...' : '🔬 Run Analysis'}
        </button>
      </div>

      {error && (
        <div style={{ padding: '0.75rem', background: '#fee2e2', border: '1px solid #fca5a5', borderRadius: '8px', marginBottom: '1rem', color: '#991b1b' }}>
          {error}
        </div>
      )}

      {!profile && !error && (
        <div className="gu-empty">
          <div className="gu-empty-icon">👤</div>
          <h3>Profile Required</h3>
          <p>Create your farmer profile first to run feasibility analysis.</p>
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
            {results.map((rec, i) => (
              <div
                key={rec.business_id}
                className="gu-card"
                style={{
                  cursor: 'pointer',
                  border: selectedRec?.business_id === rec.business_id ? '2px solid var(--gu-primary)' : undefined,
                }}
                onClick={() => setSelectedRec(rec)}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <ScoreRing score={rec.feasibility_score} size={80} label={rec.classification} />
                  <div style={{ flex: 1 }}>
                    <h3 style={{ margin: '0 0 0.25rem' }}>{i === 0 ? '🏆 ' : ''}{rec.business_name}</h3>
                    <span className={`gu-badge gu-badge-${rec.classification.toLowerCase()}`}>{rec.classification} Feasibility</span>
                    <div style={{ marginTop: '0.5rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.25rem', fontSize: '0.8rem' }}>
                      <span>💰 ₹{rec.expected_profit?.toLocaleString()}/mo</span>
                      <span>📅 {rec.break_even_months} mo break-even</span>
                      <span>📊 {rec.demand_level} demand</span>
                      <span>⚠️ {rec.risk_level} risk</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Detailed View */}
          {selectedRec && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
              <div className="gu-card">
                <h3 style={{ margin: '0 0 1rem' }}>📊 Factor Analysis — {selectedRec.business_name}</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="#e2e8f0" />
                    <PolarAngleAxis dataKey="factor" tick={{ fontSize: 11 }} />
                    <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
                    <Tooltip />
                    <Radar dataKey="score" stroke="#16a34a" fill="#22c55e" fillOpacity={0.3} strokeWidth={2} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              <div className="gu-card">
                <h3 style={{ margin: '0 0 1rem' }}>📝 {t('whyRecommended')}</h3>
                <p style={{ fontSize: '0.9rem', color: 'var(--gu-text-secondary)', lineHeight: 1.6 }}>
                  {selectedRec.why_recommended}
                </p>

                <h4 style={{ margin: '1rem 0 0.5rem', color: 'var(--gu-success)' }}>✅ {t('positiveFactors')}</h4>
                <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.85rem' }}>
                  {selectedRec.positive_factors?.map((f: string, i: number) => (
                    <li key={i} style={{ marginBottom: '0.25rem' }}>{f}</li>
                  ))}
                </ul>

                <h4 style={{ margin: '1rem 0 0.5rem', color: 'var(--gu-danger)' }}>⚠️ {t('riskFactors')}</h4>
                <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.85rem' }}>
                  {selectedRec.risk_factors?.map((f: string, i: number) => (
                    <li key={i} style={{ marginBottom: '0.25rem' }}>{f}</li>
                  ))}
                </ul>

                <div style={{ marginTop: '1rem', padding: '0.75rem', background: 'var(--gu-surface-alt)', borderRadius: '8px', fontSize: '0.85rem' }}>
                  <strong>Explanation:</strong> {selectedRec.explanation}
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* Past Assessments */}
      {assessments.length > 0 && (
        <div className="gu-card" style={{ marginTop: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1rem' }}>📋 {t('recentAssessments')}</h3>
          <table className="gu-table">
            <thead>
              <tr>
                <th>Business</th>
                <th>{t('district')}</th>
                <th>{t('score')}</th>
                <th>Classification</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {assessments.slice(0, 10).map((a) => (
                <tr key={a.id}>
                  <td style={{ fontWeight: 600 }}>{a.business_name}</td>
                  <td>{a.district}</td>
                  <td>{a.feasibility_score}</td>
                  <td><span className={`gu-badge gu-badge-${a.classification.toLowerCase()}`}>{a.classification}</span></td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--gu-text-secondary)' }}>{a.created_at ? new Date(a.created_at).toLocaleDateString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default FeasibilityAnalysis;
