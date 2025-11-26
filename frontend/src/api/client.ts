import axios, { AxiosError } from "axios";
import type { LoginPayload, TokenResponse } from "@/types/auth";

const baseURL =
  import.meta.env.VITE_API_BASE_URL?.toString() ?? "http://127.0.0.1:5002";

export const api = axios.create({
  baseURL,
  timeout: 10000
});

// Cliente con timeout extendido para operaciones largas como ETL
export const apiLong = axios.create({
  baseURL,
  timeout: 300000 // 5 minutos para operaciones largas como ETL
});

export function setAuthToken(token?: string | null) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
    apiLong.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
    delete apiLong.defaults.headers.common.Authorization;
  }
}

export async function get<T>(url: string) {
  const { data } = await api.get<T>(url);
  return data;
}

export async function post<T>(url: string, payload?: unknown) {
  const { data } = await api.post<T>(url, payload);
  return data;
}

export async function postLong<T>(url: string, payload?: unknown) {
  const { data } = await apiLong.post<T>(url, payload);
  return data;
}

export function isAxiosError(error: unknown): error is AxiosError {
  return axios.isAxiosError(error);
}

export async function loginRequest(payload: LoginPayload) {
  const { data } = await api.post<TokenResponse>("/auth/login", payload);
  return data;
}

