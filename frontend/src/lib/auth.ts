import { apiFetch } from "./api";
import type { MeResponse, LoginResponse } from "@/types/auth";

export async function login(
  username: string,
  password: string
): Promise<LoginResponse> {
  return apiFetch<LoginResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export async function logout(): Promise<void> {
  await apiFetch("/api/auth/logout", { method: "POST" });
}

export async function getMe(): Promise<MeResponse> {
  return apiFetch<MeResponse>("/api/auth/me");
}
