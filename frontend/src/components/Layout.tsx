import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import Sidebar from './Sidebar';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import type { Language } from '../i18n/translations';

const Layout: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { lang, setLang, t } = useLanguage();

  if (!isAuthenticated) return <Navigate to="/" replace />;

  return (
    <div>
      <Sidebar />
      <div className="gu-main">
        <header className="gu-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600, color: 'var(--gu-text)' }}>
              {t('welcome')}, {user?.full_name}
            </h2>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <select
              className="gu-select"
              style={{ width: 'auto', padding: '0.35rem 0.5rem', fontSize: '0.8rem' }}
              value={lang}
              onChange={(e) => setLang(e.target.value as Language)}
            >
              <option value="en">English</option>
              <option value="hi">हिन्दी</option>
              <option value="mr">मराठी</option>
            </select>
            <button className="gu-btn gu-btn-secondary gu-btn-sm" onClick={logout}>
              {t('logout')}
            </button>
          </div>
        </header>
        <main className="gu-content animate-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
