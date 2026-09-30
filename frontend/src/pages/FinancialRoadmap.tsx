import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { getUserAssessments, calculateFinancial, getFinancialPlan } from '../api/client';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = ['#16a34a', '#2563eb', '#f59e0b', '#dc2626', '#7c3aed'];

const FinancialRoadmap: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [assessments, setAssessments] = useState<any[]>([]);
  const [selectedAssessmentId, setSelectedAssessmentId] = useState<number | null>(null);
  const [plan, setPlan] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [interestRate, setInterestRate] = useState(8.5);
  const [repaymentMonths, setRepaymentMonths] = useState(60);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getUserAssessments(user!.id);
        setAssessments(res.data);
        if (res.data.length > 0) {
          setSelectedAssessmentId(res.data[0].id);
        }
      } catch {}
    };
    load();
  }, []);

  const loadPlan = async (assessmentId: number) => {
    try {
      const res = await getFinancialPlan(assessmentId);
      setPlan(res.data);
    } catch {
      setPlan(null);
    }
  };

  useEffect(() => {
    if (selectedAssessmentId) loadPlan(selectedAssessmentId);
  }, [selectedAssessmentId]);

  const calculatePlan = async () => {
    if (!selectedAssessmentId) return;
    setLoading(true);
    setError('');
    try {
      const res = await calculateFinancial({
        assessment_id: selectedAssessmentId,
        loan_interest_rate: interestRate,
        repayment_months: repaymentMonths,
      });
      setPlan(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Calculation failed.');
    } finally {
      setLoading(false);
    }
  };

  const costBreakdown = plan ? [
    { name: 'Fixed Cost', value: plan.fixed_cost },
    { name: 'Working Capital', value: plan.working_capital },
  ] : [];

  const fundingBreakdown = plan ? [
    { name: 'Your Contribution', value: plan.user_contribution },
    { name: 'Loan Required', value: plan.loan_amount },
  ] : [];

  return (
    <div>
      <h1 className="page-title">💰 {t('financialRoadmap')}</h1>

      {assessments.length === 0 ? (
        <div className="gu-empty">
          <div className="gu-empty-icon">📈</div>
          <h3>No Assessments Available</h3>
          <p>Run a feasibility analysis first to generate financial plans.</p>
        </div>
      ) : (
        <>
          {/* Controls */}
          <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ margin: '0 0 1rem' }}>⚙️ Configuration</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', alignItems: 'end' }}>
              <div>
                <label className="gu-label">Select Assessment</label>
                <select
                  className="gu-select"
                  value={selectedAssessmentId || ''}
                  onChange={(e) => setSelectedAssessmentId(Number(e.target.value))}
                >
                  {assessments.map((a) => (
                    <option key={a.id} value={a.id}>
                      {a.business_name} — {a.district} ({a.feasibility_score}/100)
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="gu-label">Interest Rate (%)</label>
                <input className="gu-input" type="number" value={interestRate} onChange={(e) => setInterestRate(Number(e.target.value))} min={0} max={30} step={0.5} />
              </div>
              <div>
                <label className="gu-label">Repayment Period ({t('months')})</label>
                <input className="gu-input" type="number" value={repaymentMonths} onChange={(e) => setRepaymentMonths(Number(e.target.value))} min={12} max={240} />
              </div>
              <button className="gu-btn gu-btn-primary" onClick={calculatePlan} disabled={loading}>
                {loading ? '⏳ Calculating...' : '🧮 Calculate'}
              </button>
            </div>
          </div>

          {error && (
            <div style={{ padding: '0.75rem', background: '#fee2e2', borderRadius: '8px', marginBottom: '1rem', color: '#991b1b' }}>
              {error}
            </div>
          )}

          {/* Financial Plan */}
          {plan && (
            <div className="animate-in">
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
                {[
                  { label: t('projectCost'), value: `₹${plan.project_cost.toLocaleString()}`, icon: '🏗️' },
                  { label: 'Your Contribution', value: `₹${plan.user_contribution.toLocaleString()}`, icon: '💵' },
                  { label: t('loanAmount'), value: `₹${plan.loan_amount.toLocaleString()}`, icon: '🏦' },
                  { label: t('emi'), value: `₹${plan.emi.toLocaleString()}`, icon: '📅' },
                  { label: 'Revenue/mo', value: `₹${plan.expected_monthly_revenue.toLocaleString()}`, icon: '💹' },
                  { label: t('monthlyProfit'), value: `₹${plan.monthly_profit.toLocaleString()}`, icon: '💰', color: plan.monthly_profit > 0 ? '#16a34a' : '#dc2626' },
                  { label: t('annualIncome'), value: `₹${plan.annual_income.toLocaleString()}`, icon: '📆' },
                  { label: t('breakEven'), value: `${plan.break_even_months} ${t('months')}`, icon: '⏱️' },
                ].map((item) => (
                  <div key={item.label} className="stat-card">
                    <div className="stat-icon" style={{ background: '#f0fdf4' }}>{item.icon}</div>
                    <div className="stat-content">
                      <h4>{item.label}</h4>
                      <p style={{ fontSize: '1.15rem', color: (item as any).color }}>{item.value}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Charts */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
                <div className="gu-card">
                  <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>🏗️ Cost Breakdown</h3>
                  <ResponsiveContainer width="100%" height={220}>
                    <PieChart>
                      <Pie data={costBreakdown} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                        {costBreakdown.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                      </Pie>
                      <Tooltip formatter={(val: number) => `₹${val.toLocaleString()}`} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="gu-card">
                  <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>💵 Funding Sources</h3>
                  <ResponsiveContainer width="100%" height={220}>
                    <PieChart>
                      <Pie data={fundingBreakdown} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                        {fundingBreakdown.map((_, i) => <Cell key={i} fill={COLORS[i + 2]} />)}
                      </Pie>
                      <Tooltip formatter={(val: number) => `₹${val.toLocaleString()}`} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Key Metrics */}
              <div className="gu-card">
                <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>📊 Key Financial Metrics</h3>
                <table className="gu-table">
                  <tbody>
                    <tr><td style={{ fontWeight: 600 }}>Interest Rate</td><td>{plan.interest_rate}% p.a.</td></tr>
                    <tr><td style={{ fontWeight: 600 }}>Repayment Period</td><td>{plan.repayment_months} months ({(plan.repayment_months / 12).toFixed(1)} years)</td></tr>
                    <tr><td style={{ fontWeight: 600 }}>Monthly Expenses</td><td>₹{plan.monthly_expenses.toLocaleString()}</td></tr>
                    {plan.roi_percentage && <tr><td style={{ fontWeight: 600 }}>{t('roi')}</td><td>{plan.roi_percentage}%</td></tr>}
                    {plan.dscr && plan.dscr < 99 && <tr><td style={{ fontWeight: 600 }}>DSCR (Debt Service Coverage)</td><td>{plan.dscr} {plan.dscr >= 1.25 ? '✅ Healthy' : '⚠️ Below threshold'}</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default FinancialRoadmap;
