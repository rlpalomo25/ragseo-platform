export interface User {
  id: string;
  username: string;
  role: "admin" | "writer";
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

export interface MeResponse {
  id: string;
  username: string;
  role: "admin" | "writer";
}

export interface LoginResponse {
  token: string;
  user: MeResponse;
}
