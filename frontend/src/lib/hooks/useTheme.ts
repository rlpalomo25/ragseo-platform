"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "ragseo-theme";

export function useTheme() {
  // Read the stored preference during the initial render instead of in an effect:
  // a read-effect would run after the write-effect's first pass and clobber the
  // stored value back to "light" before the state update landed, flashing dark
  // users. The typeof guard keeps SSR (App Router renders on the server) safe.
  const [dark, setDark] = useState<boolean>(() => {
    if (typeof window === "undefined") return false;
    return window.localStorage.getItem(STORAGE_KEY) === "dark";
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    window.localStorage.setItem(STORAGE_KEY, dark ? "dark" : "light");
  }, [dark]);

  return { dark, toggle: () => setDark((d) => !d) };
}