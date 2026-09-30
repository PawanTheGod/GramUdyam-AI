import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// Attach token from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('gu_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('gu_token');
      localStorage.removeItem('gu_user');
      window.location.href = '/';
    }
    return Promise.reject(err);
  }
);

export default api;

// ── Auth ──────────────────────────────────────────────────────────
export const demoLogin = (role: string, language: string = 'en') =>
  api.post('/auth/demo-login', { role, language });

// ── Profiles ─────────────────────────────────────────────────────
export const getProfile = () => api.get('/profiles');
export const saveProfile = (data: any) => api.post('/profiles', data);

// ── Local Data ───────────────────────────────────────────────────
export const getLocalData = (district: string) => api.get(`/local-data/${district}`);
export const listLocalData = () => api.get('/local-data');

// ── Businesses ───────────────────────────────────────────────────
export const listBusinesses = () => api.get('/businesses');
export const getBusiness = (id: number) => api.get(`/businesses/${id}`);

// ── Feasibility ──────────────────────────────────────────────────
export const analyzeFeasibility = (data: { user_id: number; district: string; business_id?: number }) =>
  api.post('/feasibility/analyze', data);
export const getUserAssessments = (userId: number) => api.get(`/feasibility/assessments/${userId}`);

// ── Financial ────────────────────────────────────────────────────
export const calculateFinancial = (data: { assessment_id: number; loan_interest_rate?: number; repayment_months?: number }) =>
  api.post('/financial/calculate', data);
export const getFinancialPlan = (assessmentId: number) => api.get(`/financial/plan/${assessmentId}`);

// ── Schemes ──────────────────────────────────────────────────────
export const listSchemes = () => api.get('/schemes');
export const matchSchemes = (data: { business_category: string; district: string; user_capital?: number }) =>
  api.post('/schemes/match', data);

// ── Dashboard ────────────────────────────────────────────────────
export const getDashboard = () => api.get('/dashboard');
export const getAdminDashboard = () => api.get('/dashboard/admin');

// ── Reports ──────────────────────────────────────────────────────
export const generateReport = (assessmentId: number) =>
  api.post(`/reports/generate?assessment_id=${assessmentId}`, {}, { responseType: 'blob' });

// ── Demo ─────────────────────────────────────────────────────────
export const runDemoAssessment = (data: any) => api.post('/demo/run-assessment', data);
