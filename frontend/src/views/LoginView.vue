<template>
  <div class="login-page">
    <section class="login-card">
      <RouterLink class="back-link" to="/">
        ← {{ $t('auth.backHome') }}
      </RouterLink>
      <h1>{{ $t('auth.loginTitle') }}</h1>
      <p class="hint">
        {{ $t('auth.loginHintLong') }}
      </p>
      <form class="login-form" @submit.prevent="handleSubmit">
        <label>
          {{ $t('auth.username') }}
          <input
            v-model.trim="username"
            name="username"
            autocomplete="username"
            required
          />
        </label>

        <label>
          {{ $t('auth.password') }}
          <input
            v-model="password"
            type="password"
            name="password"
            autocomplete="current-password"
            required
          />
        </label>

        <button type="submit" :disabled="loading || submitting">
          <span v-if="loading || submitting">
            {{ $t('auth.signingIn') }}
          </span>
          <span v-else>{{ $t('auth.loginCta') }}</span>
        </button>
      </form>

      <p v-if="formError" class="error">{{ formError }}</p>
      <p v-else-if="authError" class="error">{{ authError }}</p>
      <p v-if="success" class="success">
        {{ $t('auth.loginSuccess') }}
      </p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@composables/useAuth";

const router = useRouter();
const auth = useAuth();
const { loading } = auth;
const authError = auth.error;
const username = ref("");
const password = ref("");
const formError = ref<string | null>(null);
const success = ref(false);
const submitting = ref(false);

const handleSubmit = async () => {
  formError.value = null;
  success.value = false;
  submitting.value = true;
  try {
    if (!username.value || !password.value) {
      formError.value = "Completa usuario y contraseña.";
      return;
    }
    await auth.login({
      username: username.value,
      password: password.value
    });
    password.value = "";
    success.value = true;
    await router.push({ name: "home" });
  } catch {
    formError.value = authError.value ?? "No se pudo iniciar sesión.";
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  background: var(--bg);
}

.login-card {
  width: min(420px, 100%);
  background: var(--surface);
  border-radius: 24px;
  border: 1px solid var(--border);
  padding: 32px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.back-link {
  text-decoration: none;
  color: var(--primary);
  font-weight: 600;
  font-size: 0.9rem;
}

.hint {
  font-size: 0.9rem;
  color: var(--muted);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;

  label {
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 0.9rem;
    color: var(--text);

    input {
      border-radius: 10px;
      border: 1px solid var(--border);
      padding: 10px 14px;
      background: var(--bg);
      color: var(--text);
    }
  }

  button {
    border: none;
    border-radius: 10px;
    background: var(--primary);
    color: white;
    padding: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}

.error {
  color: var(--error-red-light);
  font-size: 0.9rem;
}

.success {
  color: var(--primary);
  font-size: 0.9rem;
}

@media (max-width: 640px) {
  .login-page {
    padding: 16px;
  }

  .login-card {
    padding: 24px;
  }
}
</style>

