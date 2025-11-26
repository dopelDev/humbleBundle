<template>
  <button
    v-if="isAuthenticated"
    class="logout-btn"
    type="button"
    @click="handleLogout"
    :aria-label="$t('auth.logout')"
  >
    <span class="logout-btn__icon" aria-hidden="true">⏏️</span>
    <div class="logout-btn__content">
      <span class="logout-btn__label">{{ $t('auth.logout') }}</span>
      <span class="logout-btn__user" v-if="currentUser?.username">
        {{ currentUser.username }}
      </span>
    </div>
  </button>
</template>

<script setup lang="ts">
import { useAuth } from "@composables/useAuth";

const auth = useAuth();
const { isAuthenticated, currentUser } = auth;

const handleLogout = () => {
  auth.logout();
};
</script>

<style scoped lang="scss">
.logout-btn {
  position: fixed;
  top: 24px;
  right: 360px;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.4rem 1rem 0.4rem 0.7rem;
  border-radius: 999px;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  font-weight: 600;
  font-size: 0.9rem;
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
    top: auto;
    right: 16px;
    bottom: 120px;
    font-size: 0.85rem;
  }
}

.logout-btn__icon {
  font-size: 1rem;
  opacity: 0.85;
}

.logout-btn__content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.1;
}

.logout-btn__label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.65rem;
  opacity: 0.9;
}

.logout-btn__user {
  font-size: 0.7rem;
  color: var(--muted);
}
</style>


