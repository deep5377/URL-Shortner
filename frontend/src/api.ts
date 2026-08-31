import type { Analytics, Metrics, ShortUrl, Workflow } from "./types";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { headers: { "Content-Type": "application/json", ...options?.headers }, ...options });
  if (!response.ok) { const body = await response.json().catch(() => null); throw new Error(body?.detail || `Request failed (${response.status})`); }
  return response.status === 204 ? (undefined as T) : response.json();
}

export const api = {
  health: () => request<{ status: string }>("/health"),
  startWorkflow: (requirement: string) => request<Workflow>("/api/v1/workflows", { method: "POST", body: JSON.stringify({ requirement }) }),
  getWorkflow: (id: string) => request<Workflow>(`/api/v1/workflows/${id}`),
  getWorkflows: () => request<Workflow[]>("/api/v1/workflows"),
  clarify: (id: string, clarification: string) => request<Workflow>(`/api/v1/workflows/${id}/clarify`, { method: "POST", body: JSON.stringify({ clarification }) }),
  rollback: (id: string) => request<Workflow>(`/api/v1/workflows/${id}/rollback`, { method: "POST" }),
  approve: (id: string, approver: string) => request<Workflow>(`/api/v1/workflows/${id}/approve`, { method: "POST", body: JSON.stringify({ approver }) }),
  reject: (id: string, approver: string, reason: string) => request<Workflow>(`/api/v1/workflows/${id}/reject`, { method: "POST", body: JSON.stringify({ approver, reason }) }),
  metrics: () => request<Metrics>("/api/v1/metrics"),
  createShortUrl: (url: string, expiresAt?: string) => request<ShortUrl>("/api/v1/urls", { method: "POST", body: JSON.stringify({ url, ...(expiresAt ? { expires_at: new Date(expiresAt).toISOString() } : {}) }) }),
  getAnalytics: (code: string) => request<Analytics>(`/api/v1/urls/${code}/analytics`),
};