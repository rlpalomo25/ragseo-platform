const API_URL = process.env.NEXT_PUBLIC_API_URL || "";

function handleUnauthorized(res: Response): void {
  if (res.status !== 401) return;
  if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
    window.location.href = "/login";
  }
  throw new Error("Unauthorized");
}

async function parseError(res: Response): Promise<Error> {
  try {
    const body = await res.json();
    return new Error(body.detail || `Request failed: ${res.status}`);
  } catch {
    return new Error(`Request failed: ${res.status}`);
  }
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  handleUnauthorized(res);
  if (!res.ok) throw await parseError(res);

  return res.json();
}

export async function apiUpload<T>(
  path: string,
  formData: FormData
): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    credentials: "include",
    body: formData,
  });

  handleUnauthorized(res);
  if (!res.ok) throw await parseError(res);

  return res.json();
}
