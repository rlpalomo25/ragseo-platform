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

function filenameFromHeader(res: Response): string | null {
  const header = res.headers.get("Content-Disposition");
  if (!header) return null;
  const match = header.match(/filename="?([^";]+)"?/);
  return match ? match[1] : null;
}

export async function apiDownload(path: string, fallbackName: string): Promise<void> {
  const res = await fetch(`${API_URL}${path}`, {
    credentials: "include",
  });

  handleUnauthorized(res);
  if (!res.ok) throw await parseError(res);

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filenameFromHeader(res) || fallbackName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
