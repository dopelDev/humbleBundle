## Stack Frontend `simpleAbout`

- **Framework**: Vue 3 (Composition API) + TypeScript.
- **Bundler**: Webpack 5 (config en `webpack.config.mjs`), con alias `@`, `@components`, `@composables`, `@style`, `@assets`.
- **Entrada**: `src/index.ts` (monta `App.vue`) + `src/index.html` como plantilla de `HtmlWebpackPlugin`.
- **Estilos**:
  - SCSS modular con `@style/reset.scss`, `@style/colors.scss`, `@style/fonts.scss`, importados vía `@style/main.scss`.
  - Tema claro/oscuro usando variables CSS (`--bg`, `--text`, etc.) actualizadas por `useDarkMode`.
  - Fuente personalizada `MonofurNerdFont` (`@font-face` en `fonts.scss`).
- **Responsive helpers**:
  - `useResponsiveQueryEvent(breakpoint=768)` para conmutar layouts (Header, App).
  - `useDarkMode` gestiona `localStorage` y clase `body.dark`.
- **Componentes clave**:
  - `Header` con variantes Desktop/Mobile, menú interactivo y botón de modo oscuro.
  - `MobileMain/Profile` como plantilla mobile (foto + redes).
  - `DesktopMain` placeholder (por completar).
- **Linter**: ESLint 9 + @typescript-eslint + eslint-plugin-vue, reglas personalizadas (indent 2 spaces, comillas dobles, semicolons).
- **Scripts npm**: `dev` (webpack-dev-server), `build` (webpack prod), `test` (webpack --version).

## Elementos para replicar

1. **SCSS global** (reset, paleta, fuente) y mixin de dark mode.
2. **Composables** `useResponsiveQueryEvent` y `useDarkMode`.
3. **Header responsive** con `DarkButton`, animaciones hover y overlay móvil.
4. **Layout Mobile/Desktop** controlado por `isMobile`.
5. **Aliases** y convención de rutas `@components/...`.
6. **Tipografía monoespaciada + iconografía (requiere fuente NerdFont).`

