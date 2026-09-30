import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { getDashboard, runDemoAssessment } from '../api/client';
import ScoreRing from '../components/ScoreRing';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [demoLoading, setDemoLoading] = useState(false);
  const [demoResult, setDemoResult] = useState<any>(null);

  const fetchDashboard = async () => {
    try {
      const res = await getDashboard();
      setData(res.data);
    } catch (err: any) {
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchDashboard(); }, []);

  const handleDemoScenario = async () => {
    setDemoLoading(true);
    try {
      const res = await runDemoAssessment({
        village: 'Sangamner',
        district: 'Ahmednagar',
        state: 'Maharashtra',
        capital: 100000,
        interest: 'Rural/agricultural business',
        language: 'mr',
      });
      setDemoResult(res.data);
      await fetchDashboard();
    } catch (err: any) {
      alert('Demo assessment failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setDemoLoading(false);
    }
  };

  if (loading) return <div className="gu-spinner" />;

  const seasonalData = data?.market_summary?.seasonal_demand
    ? Object.entries(data.market_summary.seasonal_demand).map(([month, value]) => ({
        month, demand: ((value as number) * 100),
      }))
    : [];

  const bizData = data?.market_summary?.existing_businesses
    ? Object.entries(data.market_summary.existing_businesses).map(([name, count]) => ({
        name: name.replace(/_/g, ' '), count,
      }))
    : [];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 className="page-title" style={{ margin: 0 }}>📊 {t('dashboard')}</h1>
        <button
          className="gu-btn gu-btn-accent gu-btn-lg"
          onClick={handleDemoScenario}
          disabled={demoLoading}
        >
          {demoLoading ? '⏳ Running...' : '🚀 '+ t('runAssessment') + ' (Sangamner Demo)'}
        </button>
      </div>

      {/* Demo Result Banner */}
      {demoResult && (
        <div className="gu-card animate-in" style={{ marginBottom: '1.5rem', border: '2px solid var(--gu-success)', background: '#f0fdf4' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '1.5rem' }}>✅</span>
            <h3 style={{ margin: 0, color: 'var(--gu-primary)' }}>Assessment Complete!</h3>
          </div>
          <p style={{ margin: '0 0 1rem', color: 'var(--gu-text-secondary)' }}>{demoResult.summary}</p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            {demoResult.recommendations?.map((rec: any, i: number) => (
              <div key={i} className="gu-card" style={{ background: i === 0 ? '#fefce8' : 'white' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <ScoreRing score={rec.feasibility_score} size={70} />
                  <div>
                    <h4 style={{ margin: 0 }}>{i === 0 ? '🏆 ' : ''}{rec.business_name}</h4>
                    <span className={`gu-badge gu-badge-${rec.classification.toLowerCase()}`}>{rec.classification}</span>
                    <div style={{ fontSize: '0.85rem', color: 'var(--gu-text-secondary)', marginTop: '0.25rem' }}>
                      Profit: ₹{rec.expected_profit?.toLocaleString()}/mo | Break-even: {rec.break_even_months} mo
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stats Row */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#dbeafe', color: '#2563eb' }}>📋</div>
          <div className="stat-content">
            <h4>{t('totalAssessments')}</h4>
            <p>{data?.stats?.total_assessments || 0}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#dcfce7', color: '#16a34a' }}>📈</div>
          <div className="stat-content">
            <h4>Avg {t('score')}</h4>
            <p>{data?.stats?.avg_score || 0}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fef3c7', color: '#d97706' }}>🏛️</div>
          <div className="stat-content">
            <h4>{t('matchedSchemes')}</h4>
            <p>{data?.matched_schemes_count || 0}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#f3e8ff', color: '#7c3aed' }}>💰</div>
          <div className="stat-content">
            <h4>{t('monthlyProfit')}</h4>
            <p>₹{(data?.financial_summary?.monthly_profit || 0).toLocaleString()}</p>
          </div>
        </div>
      </div>

      {/* Top Recommendations */}
      {data?.top_recommendations?.length > 0 && (
        <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1rem' }}>🏆 {t('topRecommendations')}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            {data.top_recommendations.map((rec: any, i: number) => (
              <div key={i} className="gu-card" style={{ cursor: 'pointer' }} onClick={() => navigate('/feasibility')}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div>
                    <h4 style={{ margin: '0 0 0.25rem' }}>{rec.business_name}</h4>
                    <span className={`gu-badge gu-badge-${rec.classification.toLowerCase()}`}>{rec.classification}</span>
                  </div>
                  <ScoreRing score={rec.feasibility_score} size={60} />
                </div>
                <div style={{ marginTop: '0.75rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.85rem' }}>
                  <div><span style={{ color: 'var(--gu-text-secondary)' }}>{t('profit')}:</span> ₹{rec.expected_profit?.toLocaleString()}/mo</div>
                  <div><span style={{ color: 'var(--gu-text-secondary)' }}>{t('risk')}:</span> {rec.risk_level}</div>
                  <div><span style={{ color: 'var(--gu-text-secondary)' }}>{t('investment')}:</span> ₹{rec.required_investment?.toLocaleString()}</div>
                  <div><span style={{ color: 'var(--gu-text-secondary)' }}>{t('breakEven')}:</span> {rec.break_even_months} mo</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Charts Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        {seasonalData.length > 0 && (
          <div className="gu-card">
            <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>📅 {t('seasonalDemand')}</h3>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={seasonalData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Line type="monotone" dataKey="demand" stroke="#16a34a" strokeWidth={2} dot={{ fill: '#16a34a' }} />
              </LineChart>
            </ResponsiveContainer>
            <div className="gu-badge gu-badge-demo" style={{ marginTop: '0.5rem' }}>{t('demoData')}</div>
          </div>
        )}
        {bizData.length > 0 && (
          <div className="gu-card">
            <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>🏢 {t('existingBusinesses')}</h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={bizData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} angle={-20} textAnchor="end" height={50} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#22c55e" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
            <div className="gu-badge gu-badge-demo" style={{ marginTop: '0.5rem' }}>{t('demoData')}</div>
          </div>
        )}
      </div>

      {/* Financial Summary */}
      {data?.financial_summary && (
        <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1rem' }}>💰 {t('financialSummary')}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
            {[
              { label: t('projectCost'), val: `₹${data.financial_summary.project_cost?.toLocaleString()}` },
              { label: t('loanAmount'), val: `₹${data.financial_summary.loan_amount?.toLocaleString()}` },
              { label: t('emi'), val: `₹${data.financial_summary.emi?.toLocaleString()}` },
              { label: t('monthlyProfit'), val: `₹${data.financial_summary.monthly_profit?.toLocaleString()}` },
              { label: t('annualIncome'), val: `₹${data.financial_summary.annual_income?.toLocaleString()}` },
              { label: t('breakEven'), val: `${data.financial_summary.break_even_months} ${t('months')}` },
              { label: t('roi'), val: `${data.financial_summary.roi_percentage}%` },
            ].map((item) => (
              <div key={item.label} style={{ padding: '0.75rem', background: 'var(--gu-surface-alt)', borderRadius: '8px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--gu-text-secondary)', marginBottom: '0.25rem' }}>{item.label}</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700 }}>{item.val}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!data?.top_recommendations?.length && !demoResult && (
        <div className="gu-empty">
          <div className="gu-empty-icon">📋</div>
          <h3>No assessments yet</h3>
          <p>Click the "Run Assessment" button above to start with the Sangamner demo scenario, or create your profile and run a custom analysis.</p>
          <div style={{ marginTop: '1rem', display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
            <button className="gu-btn gu-btn-primary" onClick={() => navigate('/profile')}>
              Create Profile
            </button>
            <button className="gu-btn gu-btn-accent" onClick={handleDemoScenario} disabled={demoLoading}>
              {demoLoading ? 'Running...' : 'Run Demo Scenario'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
