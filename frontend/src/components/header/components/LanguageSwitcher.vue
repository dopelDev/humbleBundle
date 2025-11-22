<template>
  <button
    class="language-switcher-btn"
    type="button"
    @click="toggleLanguage"
    :aria-label="$t('language.switch')"
    :title="$t('language.switch')"
  >
    <span class="language-switcher-btn__icon" aria-hidden="true">
      {{ currentLocale === "en" ? "🇺🇸" : "🇪🇸" }}
    </span>
    <span class="language-switcher-btn__label">
      {{
        currentLocale === "en" ? $t("language.english") : $t("language.spanish")
      }}
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";

const { locale } = useI18n();

const currentLocale = computed(() => locale.value);

const toggleLanguage = () => {
  locale.value = locale.value === "en" ? "es" : "en";
  // Persist language preference in localStorage
  localStorage.setItem("preferred-language", locale.value);
};
</script>

<style scoped lang="scss">
.language-switcher-btn {
  position: fixed;
  top: 24px;
  right: 220px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  font-weight: 500;
  font-size: 0.95rem;
  box-shadow: 0 2px 8px var(--shadow-black-light);
  cursor: pointer;
  transition: all 0.25s ease;
  z-index: 1000;

  &:hover {
    background: var(--border);
    box-shadow: 0 4px 12px var(--shadow-black);
  }

  &:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
  }

  @media (max-width: 768px) {
    position: fixed;
    top: auto;
    right: 16px;
    bottom: 80px;
    font-size: 0.85rem;
    padding: 0.35rem 0.75rem;
  }

  @media (min-width: 769px) and (max-width: 1200px) {
    right: 240px;
  }
}

.language-switcher-btn__icon {
  font-size: 1.2rem;
  opacity: 0.9;
}

.language-switcher-btn__label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.7rem;
  opacity: 0.9;
}
</style>
