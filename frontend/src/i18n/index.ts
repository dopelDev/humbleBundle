import { createI18n } from 'vue-i18n';
import es from './locales/es';
import en from './locales/en';

// Get preferred language from localStorage or default to English
const getInitialLocale = (): string => {
  const saved = localStorage.getItem('preferred-language');
  if (saved === 'es' || saved === 'en') {
    return saved;
  }
  return 'en'; // Default language: English
};

const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: 'es',
  messages: {
    es,
    en,
  },
});

export default i18n;

