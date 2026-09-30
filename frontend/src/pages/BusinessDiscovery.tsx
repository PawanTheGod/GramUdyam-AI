import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { listBusinesses, getLocalData } from '../api/client';
import type { Language } from '../i18n/translations';

const BusinessDiscovery: React.FC = () => {
  const { t, lang } = useLanguage();
  const [businesses, setBusinesses] = useState<any[]>([]);
  const [localData, setLocalData] = useState<any>(null);
  const [selectedDistrict, setSelectedDistrict] = useState('Ahmednagar');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [bizRes, ldRes] = await Promise.all([
          listBusinesses(),
          getLocalData(selectedDistrict),
        ]);
        setBusinesses(bizRes.data);
        setLocalData(ldRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    setLoading(true);
    load();
  }, [selectedDistrict]);

  const getName = (biz: any) => {
    if (lang === 'hi' && biz.name_hi) return biz.name_hi;
    if (lang === 'mr' && biz.name_mr) return biz.name_mr;
    return biz.name;
  };

  const getDesc = (biz: any) => {
    if (lang === 'hi' && biz.description_hi) return biz.description_hi;
    if (lang === 'mr' && biz.description_mr) return biz.description_mr;
    return biz.description;
  };

  const riskColor = (r: string) => r === 'Low' ? '#16a34a' : r === 'Medium' ? '#f59e0b' : '#dc2626';

  if (loading) return <div className="gu-spinner" />;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 className="page-title" style={{ margin: 0 }}>🔍 {t('businessDiscovery')}</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <label className="gu-label" style={{ margin: 0 }}>{t('district')}:</label>
          <select className="gu-select" style={{ width: 'auto' }} value={selectedDistrict} onChange={(e) => setSelectedDistrict(e.target.value)}>
            <option value="Ahmednagar">Ahmednagar</option>
            <option value="Pune">Pune</option>
            <option value="Nashik">Nashik</option>
          </select>
        </div>
      </div>

      {/* Local Data Summary */}
      {localData && (
        <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <h3 style={{ margin: 0 }}>📍 {localData.district} — Local Market Data</h3>
            <span className="gu-badge gu-badge-demo">{t('demoData')}</span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '0.75rem' }}>
            <div style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--gu-text-secondary)' }}>{t('population')}</div>
              <div style={{ fontWeight: 700 }}>{localData.population?.toLocaleString()}</div>
            </div>
            <div style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--gu-text-secondary)' }}>Villages</div>
              <div style={{ fontWeight: 700 }}>{localData.num_villages?.toLocaleString()}</div>
            </div>
            <div style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--gu-text-secondary)' }}>Road {t('connectivity')}</div>
              <div style={{ fontWeight: 700 }}>{localData.road_connectivity}</div>
            </div>
            <div style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--gu-text-secondary)' }}>Mandi Distance</div>
              <div style={{ fontWeight: 700 }}>{localData.mandi_distance_km} km</div>
            </div>
            <div style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--gu-text-secondary)' }}>Cold Storage</div>
              <div style={{ fontWeight: 700 }}>{localData.cold_storage_available ? '✅ Yes' : '❌ No'}</div>
            </div>
            <div style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--gu-text-secondary)' }}>Internet</div>
              <div style={{ fontWeight: 700 }}>{localData.internet_connectivity}</div>
            </div>
          </div>

          {/* Market Prices */}
          {localData.market_prices && (
            <div style={{ marginTop: '1rem' }}>
              <h4 style={{ margin: '0 0 0.5rem', fontSize: '0.9rem' }}>📊 {t('marketPrices')}</h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {Object.entries(localData.market_prices).map(([key, val]) => (
                  <span key={key} className="gu-badge gu-badge-info">
                    {key.replace(/_/g, ' ')}: ₹{String(val)}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Business Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '1rem' }}>
        {businesses.map((biz) => (
          <div key={biz.id} className="gu-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.75rem' }}>
              <div>
                <h3 style={{ margin: '0 0 0.25rem', fontSize: '1.1rem' }}>{getName(biz)}</h3>
                <span className="gu-badge gu-badge-info" style={{ textTransform: 'capitalize' }}>{biz.category.replace(/_/g, ' ')}</span>
              </div>
              <span className="gu-badge" style={{ background: riskColor(biz.risk_level) + '20', color: riskColor(biz.risk_level) }}>
                {biz.risk_level} {t('risk')}
              </span>
            </div>

            <p style={{ fontSize: '0.85rem', color: 'var(--gu-text-secondary)', margin: '0 0 1rem', lineHeight: 1.5 }}>
              {getDesc(biz)}
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.85rem' }}>
              <div>
                <span style={{ color: 'var(--gu-text-secondary)' }}>{t('investment')}:</span>
                <div style={{ fontWeight: 600 }}>₹{biz.required_investment_min.toLocaleString()} - ₹{biz.required_investment_max.toLocaleString()}</div>
              </div>
              <div>
                <span style={{ color: 'var(--gu-text-secondary)' }}>Revenue:</span>
                <div style={{ fontWeight: 600 }}>₹{biz.expected_monthly_revenue.toLocaleString()}/mo</div>
              </div>
              <div>
                <span style={{ color: 'var(--gu-text-secondary)' }}>{t('profit')}:</span>
                <div style={{ fontWeight: 600, color: 'var(--gu-success)' }}>₹{biz.estimated_monthly_profit.toLocaleString()}/mo</div>
              </div>
              <div>
                <span style={{ color: 'var(--gu-text-secondary)' }}>{t('breakEven')}:</span>
                <div style={{ fontWeight: 600 }}>{biz.break_even_months} {t('months')}</div>
              </div>
              <div>
                <span style={{ color: 'var(--gu-text-secondary)' }}>Operating Cost:</span>
                <div style={{ fontWeight: 600 }}>₹{biz.estimated_monthly_cost.toLocaleString()}/mo</div>
              </div>
              <div>
                <span style={{ color: 'var(--gu-text-secondary)' }}>Land Needed:</span>
                <div style={{ fontWeight: 600 }}>{biz.required_land} {t('acres')}</div>
              </div>
            </div>

            {/* Demand / Competition bars */}
            <div style={{ marginTop: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.25rem' }}>
                <span>{t('demand')}</span><span>{Math.round(biz.local_demand_base * 100)}%</span>
              </div>
              <div className="gu-progress"><div className="gu-progress-bar" style={{ width: `${biz.local_demand_base * 100}%`, background: '#22c55e' }} /></div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginTop: '0.5rem', marginBottom: '0.25rem' }}>
                <span>Competition</span><span>{Math.round(biz.competition_base * 100)}%</span>
              </div>
              <div className="gu-progress"><div className="gu-progress-bar" style={{ width: `${biz.competition_base * 100}%`, background: '#f59e0b' }} /></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BusinessDiscovery;
