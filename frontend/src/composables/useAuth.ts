import { computed, ref } from "vue";
import type { LoginPayload, UserInfo } from "@/types/auth";
import { isAxiosError, loginRequest, setAuthToken } from "@api/client";

const token = ref<string | null>(null);
const currentUser = ref<UserInfo | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const STORAGE_KEY = "hb-auth-session";

function persistSession() {
  if (typeof window === "undefined") {
    return;
  }
  if (token.value && currentUser.value) {
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        token: token.value,
        user: currentUser.value
      }),
    );
  } else {
    window.localStorage.removeItem(STORAGE_KEY);
  }
}

function restoreSession() {
  if (typeof window === "undefined") {
    return;
  }
  const stored = window.localStorage.getItem(STORAGE_KEY);
  if (!stored) {
    return;
  }
  try {
    const parsed = JSON.parse(stored) as { token: string; user: UserInfo };
    token.value = parsed.token;
    currentUser.value = parsed.user;
    setAuthToken(parsed.token);
  } catch {
    window.localStorage.removeItem(STORAGE_KEY);
  }
}

restoreSession();

export function useAuth() {
  const isAuthenticated = computed(() => Boolean(token.value));

  const login = async (payload: LoginPayload) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await loginRequest(payload);
      token.value = response.access_token;
      currentUser.value = response.user;
      setAuthToken(response.access_token);
      persistSession();
      return response.user;
    } catch (err) {
      if (isAxiosError(err)) {
        const detail =
          (err.response?.data as { detail?: string })?.detail ||
          err.response?.statusText ||
          "Error de autenticación";
        error.value = detail;
      } else {
        error.value = err instanceof Error ? err.message : "Error desconocido";
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    token.value = null;
    currentUser.value = null;
    setAuthToken(null);
    persistSession();
  };

  return {
    token,
    currentUser,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
  };
}

