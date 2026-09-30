import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { LanguageProvider } from './contexts/LanguageContext';
import Layout from './components/Layout';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import BusinessDiscovery from './pages/BusinessDiscovery';
import FeasibilityAnalysis from './pages/FeasibilityAnalysis';
import FinancialRoadmap from './pages/FinancialRoadmap';
import GovernmentSchemes from './pages/GovernmentSchemes';
import Reports from './pages/Reports';
import AdminDashboard from './pages/AdminDashboard';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <LanguageProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route element={<Layout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/business-discovery" element={<BusinessDiscovery />} />
              <Route path="/feasibility" element={<FeasibilityAnalysis />} />
              <Route path="/financial" element={<FinancialRoadmap />} />
              <Route path="/schemes" element={<GovernmentSchemes />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/admin" element={<AdminDashboard />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </LanguageProvider>
    </AuthProvider>
  );
};

export default App;
