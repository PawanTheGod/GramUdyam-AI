import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

const navItems = [
  { path: '/dashboard', icon: '📊', key: 'dashboard' as const },
  { path: '/profile', icon: '👤', key: 'profile' as const },
  { path: '/business-discovery', icon: '🔍', key: 'businessDiscovery' as const },
  { path: '/feasibility', icon: '📈', key: 'feasibility' as const },
  { path: '/financial', icon: '💰', key: 'financialRoadmap' as const },
  { path: '/schemes', icon: '🏛️', key: 'schemes' as const },
  { path: '/reports', icon: '📄', key: 'reports' as const },
];

const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const showAdmin = user?.role === 'admin';

  return (
    <aside className="gu-sidebar">
      <div className="gu-sidebar-brand">
        <h1>🌾 {t('appName')}</h1>
        <p>{t('tagline')}</p>
      </div>
      <nav className="gu-sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `gu-sidebar-link ${isActive ? 'active' : ''}`}
          >
            <span>{item.icon}</span>
            <span>{t(item.key)}</span>
          </NavLink>
        ))}
        {showAdmin && (
          <NavLink
            to="/admin"
            className={({ isActive }) => `gu-sidebar-link ${isActive ? 'active' : ''}`}
          >
            <span>⚙️</span>
            <span>{t('admin')}</span>
          </NavLink>
        )}
      </nav>
      <div className="gu-sidebar-footer">
        <div style={{ opacity: 0.7, fontSize: '0.75rem' }}>
          {user?.full_name} ({user?.role})
        </div>
        <div className="gu-badge gu-badge-demo" style={{ marginTop: '0.5rem' }}>
          {t('demoData')}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
