import { afterEach } from "vitest";
import { config } from "@vue/test-utils";
import i18n from "@/i18n";

// Configurar vue-i18n para los tests
config.global.plugins = [i18n];

// Configurar locale por defecto en español para los tests
i18n.global.locale.value = 'es';

// Limpiar después de cada test
afterEach(() => {
  // Limpiar el DOM
  document.body.innerHTML = "";
});

// Configuración global para tests
// Mantener console.log activo para debugging

