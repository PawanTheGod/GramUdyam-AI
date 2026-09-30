import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { getAdminDashboard } from '../api/client';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const COLORS = ['#16a34a', '#f59e0b', '#dc2626', '#2563eb', '#7c3aed', '#ec4899'];

const AdminDashboard: React.FC = () => {
  const { t } = useLanguage();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getAdminDashboard()
      .then((res) => { setData(res.data); setLoading(false); })
      .catch((err) => { setError(err.response?.data?.detail || 'Access denied'); setLoading(false); });
  }, []);

  if (loading) return <div className="gu-spinner" />;
  if (error) return (
    <div className="gu-empty">
      <div className="gu-empty-icon">🔒</div>
      <h3>{error}</h3>
      <p>Admin access required. Login as Administrator.</p>
    </div>
  );
  if (!data) return null;

  const feasDist = [
    { name: 'High', value: data.feasibility_distribution.High || 0 },
    { name: 'Medium', value: data.feasibility_distribution.Medium || 0 },
    { name: 'Low', value: data.feasibility_distribution.Low || 0 },
  ];

  return (
    <div>
      <h1 className="page-title">⚙️ {t('admin')}</h1>

      {/* Stats */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#dbeafe', color: '#2563eb' }}>👥</div>
          <div className="stat-content"><h4>Total Users</h4><p>{data.total_users}</p></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#dcfce7', color: '#16a34a' }}>📋</div>
          <div className="stat-content"><h4>{t('totalAssessments')}</h4><p>{data.total_assessments}</p></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fef3c7', color: '#d97706' }}>🏢</div>
          <div className="stat-content"><h4>Businesses Assessed</h4><p>{data.businesses_assessed}</p></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#f3e8ff', color: '#7c3aed' }}>📊</div>
          <div className="stat-content"><h4>Districts</h4><p>{data.system_status.districts_available}</p></div>
        </div>
      </div>

      {/* Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        <div className="gu-card">
          <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>📊 Feasibility Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={feasDist} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                {feasDist.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="gu-card">
          <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>📈 Popular Categories</h3>
          {data.popular_categories.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={data.popular_categories}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="category" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#22c55e" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <div className="gu-empty"><p>No data yet</p></div>}
        </div>
      </div>

      {/* District Assessments */}
      {data.district_assessments.length > 0 && (
        <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>📍 District-wise Assessments</h3>
          <table className="gu-table">
            <thead><tr><th>{t('district')}</th><th>Assessments</th></tr></thead>
            <tbody>
              {data.district_assessments.map((d: any) => (
                <tr key={d.district}><td style={{ fontWeight: 600 }}>{d.district}</td><td>{d.count}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* System Status */}
      <div className="gu-card">
        <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>🖥️ {t('systemStatus')}</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem' }}>
          {Object.entries(data.system_status).map(([key, val]) => (
            <div key={key} style={{ padding: '0.5rem', background: 'var(--gu-surface-alt)', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--gu-text-secondary)', textTransform: 'uppercase' }}>{key.replace(/_/g, ' ')}</div>
              <div style={{ fontWeight: 600 }}>{String(val)}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
