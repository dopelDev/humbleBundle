import { computed } from "vue";
import { useScrollToSection } from "@composables/useScrollToSection";

interface HeaderItem {
  name: string;
  action: () => void;
}

const LINKS = {
  about: "https://about.dopeldev.com",
  github: "https://github.com/dopeldev/humble-etl" // placeholder
};

export function useHeaderItems() {
  const { goTo } = useScrollToSection();

  const items = computed<HeaderItem[]>(() => [
    {
      name: "Bundles",
      action: () => goTo("bundles"),
    },
    {
      name: "Destacado",
      action: () => goTo("featured"),
    },
    {
      name: "Contact",
      action: () => goTo("contact"),
    },
    {
      name: "About",
      action: () => window.open(LINKS.about, "_blank", "noopener"),
    },
    {
      name: "Github",
      action: () => window.open(LINKS.github, "_blank", "noopener"),
    },
  ]);

  return { items };
}

