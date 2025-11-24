import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import vue from 'eslint-plugin-vue';
import vueParser from 'vue-eslint-parser';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{js,mjs,cjs,ts}'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      parserOptions: {
        ecmaVersion: 2022,
        sourceType: 'module',
      },
    },
    plugins: {
      '@typescript-eslint': tseslint.plugin,
    },
    rules: {
      // TypeScript específicas
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
          destructuredArrayIgnorePattern: '^_',
          ignoreRestSiblings: true,
        },
      ],
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/explicit-module-boundary-types': 'off',
      // JavaScript generales
      'no-console': ['warn', { allow: ['error', 'warn'] }],
      'no-debugger': 'warn',
      'prefer-const': 'warn',
      'no-var': 'error',
      'object-shorthand': 'warn',
      'prefer-template': 'warn',
      'no-void': 'off',
    },
  },
  ...vue.configs['flat/recommended'],
  {
    files: ['**/*.vue'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parser: vueParser,
      parserOptions: {
        parser: '@typescript-eslint/parser',
        extraFileExtensions: ['.vue'],
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
    plugins: {
      vue,
      '@typescript-eslint': tseslint.plugin,
    },
    rules: {
      // Vue 3 - Estructura y organización
      'vue/multi-word-component-names': 'off',
      'vue/no-multiple-template-root': 'off', // Vue 3 permite múltiples roots
      'vue/component-name-in-template-casing': ['warn', 'PascalCase'],
      'vue/component-definition-name-casing': ['warn', 'PascalCase'],
      
      // Vue 3 - Script Setup
      'vue/define-macros-order': ['warn', {
        order: ['defineProps', 'defineEmits', 'defineExpose']
      }],
      'vue/define-props-declaration': ['warn', 'type-based'],
      'vue/define-emits-declaration': ['warn', 'type-based'],
      
      // Props y Emits
      'vue/require-default-prop': 'off',
      'vue/require-explicit-emits': 'error',
      'vue/require-prop-types': 'off', // TypeScript ya maneja los tipos
      'vue/prop-name-casing': ['warn', 'camelCase'],
      'vue/require-prop-type-constructor': 'error',
      
      // Template - Seguridad
      'vue/no-v-html': 'warn',
      'vue/no-v-text-v-html-on-component': 'error',
      'vue/no-v-text': 'warn',
      
      // Template - Directivas (validación de uso correcto)
      'vue/no-use-v-if-with-v-for': 'error',
      'vue/no-duplicate-attributes': 'error',
      'vue/no-multiple-slot-args': 'error',
      'vue/no-template-key': 'error',
      'vue/no-v-text': 'warn',
      'vue/no-v-html': 'warn',
      'vue/no-v-text-v-html-on-component': 'error',
      
      // Template - Bindings y expresiones
      'vue/no-template-shadow': 'error',
      'vue/no-unused-vars': 'warn',
      'vue/no-unused-refs': 'warn',
      'vue/no-useless-mustaches': 'warn',
      'vue/no-useless-v-bind': 'warn',
      'vue/no-useless-concat': 'warn',
      'vue/prefer-separate-static-class': 'off',
      'vue/prefer-true-attribute-shorthand': 'warn',
      
      // Template - Eventos
      'vue/v-on-event-hyphenation': ['warn', 'always'],
      'vue/v-on-function-call': ['warn', 'never'],
      
      // Template - Componentes
      'vue/no-unused-components': 'warn',
      'vue/no-reserved-component-names': 'error',
      
      // Template - Accesibilidad
      'vue/require-toggle-inside-transition': 'error',
      'vue/require-valid-default-prop': 'error',
      
      // Template - Validación de directivas Vue (sintaxis correcta)
      'vue/valid-v-bind': 'error',
      'vue/valid-v-else': 'error',
      'vue/valid-v-else-if': 'error',
      'vue/valid-v-for': 'error',
      'vue/valid-v-if': 'error',
      'vue/valid-v-is': 'error',
      'vue/valid-v-memo': 'error',
      'vue/valid-v-on': 'error',
      'vue/valid-v-once': 'error',
      'vue/valid-v-pre': 'error',
      'vue/valid-v-show': 'error',
      'vue/valid-v-slot': 'error',
      'vue/valid-v-text': 'error',
      'vue/valid-v-model': 'error',
      'vue/valid-v-html': 'error',
      
      // Template - Interpolaciones
      'vue/mustache-interpolation-spacing': ['warn', 'always'],
      'vue/no-bare-strings-in-template': 'off', // Permitir strings sin i18n
      'vue/no-empty-component-block': 'error',
      'vue/no-multiple-objects-in-class': 'warn',
      'vue/no-parsing-error': 'error',
      'vue/no-spaces-around-equal-signs-in-attribute': 'error',
      'vue/no-textarea-mustache': 'error',
      
      // Template - Slots
      'vue/v-slot-style': ['warn', 'shorthand'],
      
      // Template - Estructura
      'vue/valid-template-root': 'error',
      
      // Template - Estilo y formato (más flexible)
      'vue/html-self-closing': 'off',
      'vue/max-attributes-per-line': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'vue/multiline-html-element-content-newline': 'off',
      'vue/attributes-order': 'off',
      'vue/html-closing-bracket-newline': 'off',
      'vue/html-indent': 'off',
      'vue/first-attribute-linebreak': 'off',
      'vue/html-quotes': ['warn', 'double'],
      'vue/mustache-interpolation-spacing': ['warn', 'always'],
      
      // Vue - Mejores prácticas
      'vue/no-unused-components': 'warn',
      'vue/no-unused-vars': 'warn',
      'vue/no-useless-template-attributes': 'warn',
      'vue/no-useless-v-bind': 'warn',
      'vue/prefer-separate-static-class': 'off',
      'vue/prefer-true-attribute-shorthand': 'warn',
      'vue/v-on-function-call': ['warn', 'never'],
      
      // Vue - Composición API
      'vue/no-ref-as-operand': 'error',
      'vue/no-setup-props-destructure': 'off', // Permitir destructuring de props
      'vue/prefer-define-options': 'warn',
      
      // Vue - Reactividad
      'vue/no-watch-after-await': 'error',
      'vue/no-async-in-computed-properties': 'error',
      'vue/no-computed-properties-in-data': 'error',
      'vue/no-dupe-keys': 'error',
      
      // Vue - Lifecycle
      'vue/no-lifecycle-after-await': 'error',
      // TypeScript específicas (aplicadas también a archivos Vue)
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
          destructuredArrayIgnorePattern: '^_',
          ignoreRestSiblings: true,
        },
      ],
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/explicit-module-boundary-types': 'off',
      // JavaScript generales
      'no-console': ['warn', { allow: ['error', 'warn'] }],
      'no-debugger': 'warn',
      'prefer-const': 'warn',
      'no-var': 'error',
      'object-shorthand': 'warn',
      'prefer-template': 'warn',
      'no-void': 'off',
    },
  },
  {
    files: ['**/*.test.{ts,js}', '**/*.spec.{ts,js}', '**/tests/**', '**/test/**'],
    rules: {
      'no-console': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
  {
    ignores: [
      'node_modules/**',
      'dist/**',
      '*.config.js',
      '*.config.ts',
      '*.config.mjs',
      'coverage/**',
      '.vite/**',
      '.tsbuild/**',
      '**/*.d.ts',
      'vite.config.ts',
    ],
  }
);

