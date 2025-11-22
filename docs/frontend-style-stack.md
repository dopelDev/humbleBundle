## Frontend Stack `simpleAbout`

- **Framework**: Vue 3 (Composition API) + TypeScript.
- **Bundler**: Webpack 5 (config in `webpack.config.mjs`), with aliases `@`, `@components`, `@composables`, `@style`, `@assets`.
- **Entry**: `src/index.ts` (mounts `App.vue`) + `src/index.html` as `HtmlWebpackPlugin` template.
- **Styles**:
  - Modular SCSS with `@style/reset.scss`, `@style/colors.scss`, `@style/fonts.scss`, imported via `@style/main.scss`.
  - Light/dark theme using CSS variables (`--bg`, `--text`, etc.) updated by `useDarkMode`.
  - Custom font `MonofurNerdFont` (`@font-face` in `fonts.scss`).
- **Responsive helpers**:
  - `useResponsiveQueryEvent(breakpoint=768)` to switch layouts (Header, App).
  - `useDarkMode` manages `localStorage` and `body.dark` class.
- **Key components**:
  - `Header` with Desktop/Mobile variants, interactive menu and dark mode button.
  - `MobileMain/Profile` as mobile template (photo + social links).
  - `DesktopMain` placeholder (to be completed).
- **Linter**: ESLint 9 + @typescript-eslint + eslint-plugin-vue, custom rules (indent 2 spaces, double quotes, semicolons).
- **npm scripts**: `dev` (webpack-dev-server), `build` (webpack prod), `test` (webpack --version).

## Elements to Replicate

1. **Global SCSS** (reset, palette, font) and dark mode mixin.
2. **Composables** `useResponsiveQueryEvent` and `useDarkMode`.
3. **Responsive Header** with `DarkButton`, hover animations and mobile overlay.
4. **Mobile/Desktop Layout** controlled by `isMobile`.
5. **Aliases** and route convention `@components/...`.
6. **Monospaced typography + iconography (requires NerdFont).**
