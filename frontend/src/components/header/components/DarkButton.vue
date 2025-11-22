<template>
  <button
    class="dark-mode-btn"
    type="button"
    @click="toggleDarkMode"
    :aria-pressed="isDarkMode"
  >
    <span class="dark-mode-btn__icon" aria-hidden="true">
      {{ isDarkMode ? "🌙" : "☀️" }}
    </span>
    <span class="dark-mode-btn__label">
      {{ isDarkMode ? "Modo oscuro" : "Modo claro" }}
    </span>
    <span class="dark-mode-btn__track" aria-hidden="true">
      <span
        class="dark-mode-btn__thumb"
        :class="{ 'dark-mode-btn__thumb--active': isDarkMode }"
      />
    </span>
  </button>
</template>

<script setup lang="ts">
import { useDarkMode } from "@composables/useDarkMode";

const { isDarkMode, toggleDarkMode } = useDarkMode();
</script>

<style scoped lang="scss">
.dark-mode-btn {
  position: fixed;
  top: 24px;
  right: 32px;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
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
    bottom: 24px;
  }
}

.dark-mode-btn__icon {
  font-size: 1.2rem;
  opacity: 0.8;
}

.dark-mode-btn__label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.7rem;
  opacity: 0.9;
}

.dark-mode-btn__track {
  width: 46px;
  height: 22px;
  background: var(--border);
  border-radius: 999px;
  padding: 3px;
  display: flex;
  align-items: center;
}

.dark-mode-btn__thumb {
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: var(--text);
  opacity: 0.7;
  transform: translateX(0);
  transition: transform 0.25s ease, background 0.25s ease, opacity 0.25s ease;

  &--active {
    transform: translateX(24px);
    background: var(--text);
    opacity: 1;
  }
}
</style>

