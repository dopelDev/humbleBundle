import { ref, onMounted, onUnmounted } from "vue";

export function useResponsiveQueryEvent(breakpoint = 768) {
  const isMobile = ref(false);
  const query = `(max-width: ${breakpoint - 1}px)`;
  let mediaQuery: MediaQueryList;

  const update = (e: MediaQueryListEvent | MediaQueryList) => {
    isMobile.value = e.matches;
  };

  onMounted(() => {
    mediaQuery = window.matchMedia(query);
    update(mediaQuery);
    mediaQuery.addEventListener("change", update);
  });

  onUnmounted(() => {
    mediaQuery?.removeEventListener("change", update);
  });

  return { isMobile };
}

