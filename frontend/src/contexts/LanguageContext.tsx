import React, { createContext, useContext, useState, ReactNode } from 'react';
import { translations, Language, TranslationKey } from '../i18n/translations';

interface LanguageContextType {
  lang: Language;
  setLang: (l: Language) => void;
  t: (key: TranslationKey) => string;
}

const LanguageContext = createContext<LanguageContextType>({
  lang: 'en',
  setLang: () => {},
  t: (key) => key,
});

export const useLanguage = () => useContext(LanguageContext);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [lang, setLang] = useState<Language>(() => {
    const saved = localStorage.getItem('gu_lang');
    return (saved as Language) || 'en';
  });

  const changeLang = (l: Language) => {
    localStorage.setItem('gu_lang', l);
    setLang(l);
  };

  const t = (key: TranslationKey): string => {
    return translations[lang]?.[key] || translations.en[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang: changeLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};
