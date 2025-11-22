/// <reference types="vitest" />
import { defineConfig } from "vitest/config";
import vue from "@vitejs/plugin-vue";
import path from "node:path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(process.cwd(), "src"),
      "@components": path.resolve(process.cwd(), "src/components"),
      "@composables": path.resolve(process.cwd(), "src/composables"),
      "@api": path.resolve(process.cwd(), "src/api"),
      "@style": path.resolve(process.cwd(), "src/style"),
      "@assets": path.resolve(process.cwd(), "src/assets")
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@style/colors.scss" as *;\n@use "@style/fonts.scss" as *;\n`
      }
    }
  },
  server: {
    port: 3002,
    strictPort: true,
    host: "0.0.0.0",
    open: false
  },
  test: {
    globals: true,
    environment: "happy-dom",
    setupFiles: ["./src/tests/setup.ts"],
    include: ["src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "src/test/",
        "**/*.d.ts",
        "**/*.config.*",
        "**/dist/**"
      ]
    }
  }
});
