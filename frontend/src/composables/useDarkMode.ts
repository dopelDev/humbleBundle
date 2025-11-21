import { onMounted, ref } from "vue";

const isDarkMode = ref(false);
let initialized = false;
let mediaQuery: MediaQueryList | null = null;

const applyTheme = (value: boolean) => {
  if (typeof document === "undefined") {
    return;
  }
  document.body.classList.toggle("dark", value);
  document.body.dataset.theme = value ? "dark" : "light";
  document.documentElement.style.setProperty("color-scheme", value ? "dark" : "light");
};

const setDarkMode = (value: boolean, persist = true) => {
  isDarkMode.value = value;
  applyTheme(value);
  if (persist && typeof window !== "undefined") {
    localStorage.setItem("darkMode", value ? "true" : "false");
  }
};

const initialize = () => {
  if (initialized || typeof window === "undefined") {
    return;
  }
  initialized = true;
  mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  const storedPreference = localStorage.getItem("darkMode");
  if (storedPreference === null) {
    setDarkMode(mediaQuery.matches, false);
  } else {
    setDarkMode(storedPreference === "true");
  }

  const handleChange = (event: MediaQueryListEvent) => {
    if (localStorage.getItem("darkMode") === null) {
      setDarkMode(event.matches, false);
    }
  };

  mediaQuery.addEventListener("change", handleChange);
};

export function useDarkMode() {
  const toggleDarkMode = () => {
    setDarkMode(!isDarkMode.value);
  };

  onMounted(() => {
    initialize();
  });

  return { isDarkMode, toggleDarkMode };
}

