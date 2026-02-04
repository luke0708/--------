export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
console.log("Current API Base:", API_BASE);

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || `请求失败: ${res.status}`);
  }
  return res.json();
}

export async function login(username, password) {
  const data = await request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  setToken(data.access_token);
  return data;
}

export async function refreshToken() {
  const data = await request("/auth/refresh", { method: "POST" });
  setToken(data.access_token);
  return data;
}

export function fetchTopics() {
  return request("/topics");
}

export function fetchSources() {
  return request("/sources");
}

export function fetchArticles(topicId, days = 3) {
  const qs = new URLSearchParams();
  if (topicId) qs.set("topic_id", topicId);
  qs.set("days", days);
  return request(`/articles?${qs.toString()}`);
}

export function createTopic(payload) {
  return request("/topics", { method: "POST", body: JSON.stringify(payload) });
}

export function updateTopic(id, payload) {
  return request(`/topics/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
}

export function createSource(payload) {
  return request("/sources", { method: "POST", body: JSON.stringify(payload) });
}

export function updateSource(id, payload) {
  return request(`/sources/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
}

export function manualFetch() {
  return request("/admin/fetch", { method: "POST" });
}

export function analyzeManual(titles) {
  return request("/analysis/manual", {
    method: "POST",
    body: JSON.stringify({ titles }),
  });
}
