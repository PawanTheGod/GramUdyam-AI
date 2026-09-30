import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { demoLogin } from '../api/client';
import type { Language } from '../i18n/translations';

const Landing: React.FC = () => {
  const { login, isAuthenticated } = useAuth();
  const { t, lang, setLang } = useLanguage();
  const navigate = useNavigate();
  const [loading, setLoading] = useState('');

  if (isAuthenticated) {
    navigate('/dashboard');
    return null;
  }

  const handleLogin = async (role: string) => {
    setLoading(role);
    try {
      const res = await demoLogin(role, lang);
      login(res.data.access_token, res.data.user);
      navigate('/dashboard');
    } catch (err) {
      alert('Login failed. Is the backend running?');
    } finally {
      setLoading('');
    }
  };

  return (
    <div>
      {/* Hero */}
      <div className="landing-hero">
        <nav className="landing-nav">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span style={{ fontSize: '1.8rem' }}>🌾</span>
            <div>
              <div style={{ fontWeight: 700, fontSize: '1.2rem' }}>{t('appName')}</div>
              <div style={{ fontSize: '0.65rem', opacity: 0.7 }}>{t('tagline')}</div>
            </div>
          </div>
          <select
            style={{
              background: 'rgba(255,255,255,0.15)',
              border: '1px solid rgba(255,255,255,0.3)',
              color: 'white',
              padding: '0.4rem 0.75rem',
              borderRadius: '6px',
              fontSize: '0.85rem',
            }}
            value={lang}
            onChange={(e) => setLang(e.target.value as Language)}
          >
            <option value="en" style={{ color: '#000' }}>English</option>
            <option value="hi" style={{ color: '#000' }}>हिन्दी</option>
            <option value="mr" style={{ color: '#000' }}>मराठी</option>
          </select>
        </nav>

        <div className="landing-content">
          <div className="landing-grid">
            <div className="landing-text">
              <h1>{t('heroTitle')}</h1>
              <p>{t('heroSubtitle')}</p>
              <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
                {[
                  { icon: '🔍', label: 'Business Discovery' },
                  { icon: '📈', label: 'Feasibility Analysis' },
                  { icon: '💰', label: 'Financial Planning' },
                  { icon: '🏛️', label: 'Scheme Matching' },
                ].map((f) => (
                  <div key={f.label} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem' }}>
                    <span style={{ fontSize: '1.3rem' }}>{f.icon}</span>
                    {f.label}
                  </div>
                ))}
              </div>
            </div>

            <div className="landing-login">
              <h2>{t('loginAs')}</h2>
              <p>{t('selectRole')}</p>

              <button
                className="login-role-btn"
                onClick={() => handleLogin('farmer')}
                disabled={!!loading}
              >
                <div className="login-role-icon">👨‍🌾</div>
                <div>
                  <div>{t('farmer')}</div>
                  <div style={{ fontSize: '0.75rem', opacity: 0.7, fontWeight: 400 }}>
                    Discover businesses, get assessments
                  </div>
                </div>
                {loading === 'farmer' && <span style={{ marginLeft: 'auto' }}>⏳</span>}
              </button>

              <button
                className="login-role-btn"
                onClick={() => handleLogin('officer')}
                disabled={!!loading}
              >
                <div className="login-role-icon">🏛️</div>
                <div>
                  <div>{t('officer')}</div>
                  <div style={{ fontSize: '0.75rem', opacity: 0.7, fontWeight: 400 }}>
                    Review assessments, monitor data
                  </div>
                </div>
                {loading === 'officer' && <span style={{ marginLeft: 'auto' }}>⏳</span>}
              </button>

              <button
                className="login-role-btn"
                onClick={() => handleLogin('admin')}
                disabled={!!loading}
              >
                <div className="login-role-icon">⚙️</div>
                <div>
                  <div>{t('administrator')}</div>
                  <div style={{ fontSize: '0.75rem', opacity: 0.7, fontWeight: 400 }}>
                    Full system access, admin dashboard
                  </div>
                </div>
                {loading === 'admin' && <span style={{ marginLeft: 'auto' }}>⏳</span>}
              </button>

              <div style={{ marginTop: '1rem', fontSize: '0.75rem', opacity: 0.6, textAlign: 'center' }}>
                Demo credentials — no signup required
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="landing-features">
        <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: 'var(--gu-primary-dark)' }}>
          How GramUdyam AI Works
        </h2>
        <div className="features-grid">
          {[
            { icon: '👤', title: 'Create Profile', desc: 'Enter your village, capital, skills, and interests.' },
            { icon: '📊', title: 'Local Market Data', desc: 'View population, businesses, prices, and infrastructure.' },
            { icon: '🤖', title: 'AI Feasibility Analysis', desc: 'Get scored business recommendations tailored to you.' },
            { icon: '💰', title: 'Financial Roadmap', desc: 'See project costs, EMI, loan details, and break-even.' },
            { icon: '🏛️', title: 'Scheme Matching', desc: 'Find eligible government subsidy and loan schemes.' },
            { icon: '📄', title: 'PDF Reports', desc: 'Generate downloadable feasibility reports.' },
            { icon: '🌐', title: 'Multi-language', desc: 'Available in English, Hindi, and Marathi.' },
            { icon: '📱', title: 'Responsive Design', desc: 'Works on desktop, tablet, and mobile devices.' },
          ].map((f) => (
            <div key={f.title} className="gu-card feature-card">
              <div className="feature-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer style={{
        background: 'var(--gu-primary-dark)', color: 'white', padding: '2rem',
        textAlign: 'center', fontSize: '0.85rem', opacity: 0.8
      }}>
        <p style={{ margin: 0 }}>
          GramUdyam AI — MVP Demo | Built for rural entrepreneurship empowerment
        </p>
        <p style={{ margin: '0.5rem 0 0', fontSize: '0.75rem', opacity: 0.6 }}>
          This is a demonstration application. All data shown is for illustrative purposes only.
        </p>
      </footer>
    </div>
  );
};

export default Landing;
