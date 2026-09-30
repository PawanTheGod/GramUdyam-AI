import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { getProfile, saveProfile } from '../api/client';

const DISTRICTS = ['Ahmednagar', 'Pune', 'Nashik'];

const Profile: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [form, setForm] = useState({
    name: user?.full_name || '',
    village: '',
    block: '',
    district: 'Ahmednagar',
    state: 'Maharashtra',
    available_capital: 100000,
    business_interest: '',
    available_land: 1,
    skills: '',
    preferred_language: 'en',
    phone: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getProfile();
        setForm((prev) => ({ ...prev, ...res.data }));
      } catch {
        // No profile yet — that's fine
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === 'available_capital' || name === 'available_land' ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSaved(false);
    if (!form.name || !form.district) {
      setError('Name and District are required.');
      return;
    }
    setSaving(true);
    try {
      await saveProfile(form);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save profile.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="gu-spinner" />;

  return (
    <div>
      <h1 className="page-title">👤 {t('profile')}</h1>

      <form onSubmit={handleSubmit} style={{ maxWidth: '700px' }}>
        <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>Personal Information</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label className="gu-label">{t('name')} *</label>
              <input className="gu-input" name="name" value={form.name} onChange={handleChange} required />
            </div>
            <div>
              <label className="gu-label">{t('phoneNumber')}</label>
              <input className="gu-input" name="phone" value={form.phone} onChange={handleChange} placeholder="+91..." />
            </div>
            <div>
              <label className="gu-label">{t('village')}</label>
              <input className="gu-input" name="village" value={form.village} onChange={handleChange} placeholder="e.g. Sangamner" />
            </div>
            <div>
              <label className="gu-label">{t('block')}</label>
              <input className="gu-input" name="block" value={form.block} onChange={handleChange} />
            </div>
            <div>
              <label className="gu-label">{t('district')} *</label>
              <select className="gu-select" name="district" value={form.district} onChange={handleChange} required>
                {DISTRICTS.map((d) => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
            <div>
              <label className="gu-label">{t('state')}</label>
              <input className="gu-input" name="state" value={form.state} onChange={handleChange} />
            </div>
          </div>
        </div>

        <div className="gu-card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1rem', fontSize: '1rem' }}>Business & Resources</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label className="gu-label">{t('capital')} (₹)</label>
              <input className="gu-input" name="available_capital" type="number" value={form.available_capital} onChange={handleChange} min={0} />
            </div>
            <div>
              <label className="gu-label">{t('land')} ({t('acres')})</label>
              <input className="gu-input" name="available_land" type="number" value={form.available_land} onChange={handleChange} min={0} step={0.1} />
            </div>
            <div style={{ gridColumn: '1 / -1' }}>
              <label className="gu-label">{t('interest')}</label>
              <input className="gu-input" name="business_interest" value={form.business_interest} onChange={handleChange} placeholder="e.g. Dairy, Food Processing" />
            </div>
            <div style={{ gridColumn: '1 / -1' }}>
              <label className="gu-label">{t('skills')} (comma-separated)</label>
              <input className="gu-input" name="skills" value={form.skills} onChange={handleChange} placeholder="e.g. agriculture, animal care, basic accounting" />
            </div>
            <div>
              <label className="gu-label">{t('language')}</label>
              <select className="gu-select" name="preferred_language" value={form.preferred_language} onChange={handleChange}>
                <option value="en">English</option>
                <option value="hi">हिन्दी</option>
                <option value="mr">मराठी</option>
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div style={{ padding: '0.75rem', background: '#fee2e2', border: '1px solid #fca5a5', borderRadius: '8px', marginBottom: '1rem', color: '#991b1b' }}>
            {error}
          </div>
        )}
        {saved && (
          <div style={{ padding: '0.75rem', background: '#dcfce7', border: '1px solid #86efac', borderRadius: '8px', marginBottom: '1rem', color: '#166534' }}>
            ✅ Profile saved successfully!
          </div>
        )}

        <button className="gu-btn gu-btn-primary gu-btn-lg" type="submit" disabled={saving}>
          {saving ? '⏳ Saving...' : `💾 ${t('save')} ${t('profile')}`}
        </button>
      </form>
    </div>
  );
};

export default Profile;
