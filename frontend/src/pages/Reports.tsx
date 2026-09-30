import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { getUserAssessments, generateReport } from '../api/client';

const Reports: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [assessments, setAssessments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState<number | null>(null);

  useEffect(() => {
    getUserAssessments(user!.id).then((res) => { setAssessments(res.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const handleGenerate = async (assessmentId: number) => {
    setGenerating(assessmentId);
    try {
      const res = await generateReport(assessmentId);
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `gramudyam_report_${assessmentId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      alert('Report generation failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setGenerating(null);
    }
  };

  if (loading) return <div className="gu-spinner" />;

  return (
    <div>
      <h1 className="page-title">📄 {t('reports')}</h1>

      {assessments.length === 0 ? (
        <div className="gu-empty">
          <div className="gu-empty-icon">📋</div>
          <h3>No Reports Available</h3>
          <p>Run a feasibility analysis first, then generate downloadable PDF reports.</p>
        </div>
      ) : (
        <div className="gu-card">
          <p style={{ margin: '0 0 1rem', color: 'var(--gu-text-secondary)', fontSize: '0.9rem' }}>
            Select an assessment to generate a comprehensive PDF feasibility report including profile, business analysis, financial calculations, and scheme matching.
          </p>
          <table className="gu-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Business</th>
                <th>{t('district')}</th>
                <th>{t('score')}</th>
                <th>Classification</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {assessments.map((a) => (
                <tr key={a.id}>
                  <td>#{a.id}</td>
                  <td style={{ fontWeight: 600 }}>{a.business_name}</td>
                  <td>{a.district}</td>
                  <td>{a.feasibility_score}/100</td>
                  <td><span className={`gu-badge gu-badge-${a.classification.toLowerCase()}`}>{a.classification}</span></td>
                  <td style={{ fontSize: '0.8rem' }}>{a.created_at ? new Date(a.created_at).toLocaleDateString() : '-'}</td>
                  <td>
                    <button
                      className="gu-btn gu-btn-primary gu-btn-sm"
                      onClick={() => handleGenerate(a.id)}
                      disabled={generating === a.id}
                    >
                      {generating === a.id ? '⏳' : '📥'} {t('generateReport')}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Reports;
