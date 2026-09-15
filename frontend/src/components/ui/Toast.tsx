"use client";

import { useEffect, useState } from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error" | "info";
  onDismiss: () => void;
}

export function Toast({ message, type = "info", onDismiss }: ToastProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(true);
    const timer = setTimeout(() => {
      setVisible(false);
      setTimeout(onDismiss, 300);
    }, 4000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  const styles = {
    success: "bg-green-600",
    error: "bg-red-600",
    info: "bg-brand-600",
  };

  return (
    <div
      className={`fixed bottom-4 right-4 z-50 rounded-lg px-4 py-3 text-sm text-white shadow-lg transition-all duration-300 ${
        styles[type]
      } ${visible ? "translate-y-0 opacity-100" : "translate-y-2 opacity-0"}`}
      role="status"
      aria-live="polite"
    >
      {message}
    </div>
  );
}
