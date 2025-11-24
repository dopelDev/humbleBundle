export default {
  extends: [
    'stylelint-config-standard-scss',
    'stylelint-config-recommended-vue',
  ],
  customSyntax: 'postcss-html',
  rules: {
    // Desactivar reglas que pueden ser muy estrictas
    'selector-class-pattern': null,
    'scss/at-import-partial-extension': null,
    'scss/at-import-no-partial-leading-underscore': null,
    
    // Permitir valores sin comillas en algunos casos
    'value-keyword-case': ['lower', {
      ignoreKeywords: ['currentColor', 'inherit', 'initial', 'unset', 'revert']
    }],
    
    // Flexibilidad con unidades
    'unit-allowed-list': null,
    'declaration-property-value-allowed-list': null,
    
    // Permitir anidamiento profundo (común en SCSS)
    'max-nesting-depth': null,
    
    // Flexibilidad con selectores
    'selector-pseudo-class-no-unknown': [true, {
      ignorePseudoClasses: ['deep', 'global', 'slotted']
    }],
    'selector-pseudo-element-no-unknown': [true, {
      ignorePseudoElements: ['v-deep', 'v-global', 'v-slotted']
    }],
    
    // Permitir @apply de Tailwind si se usa en el futuro
    'at-rule-no-unknown': [true, {
      ignoreAtRules: ['apply', 'layer', 'variants', 'responsive', 'screen', 'function', 'if', 'each', 'include', 'mixin', 'use', 'forward', 'return', 'warn', 'error']
    }],
    
    // Flexibilidad con propiedades personalizadas (CSS variables)
    'property-no-unknown': [true, {
      ignoreProperties: ['composes', '/^--/']
    }],
    
    // Permitir comentarios en línea
    'comment-empty-line-before': null,
    'comment-whitespace-inside': null,
    
    // Flexibilidad con orden de propiedades
    'declaration-block-no-duplicate-properties': true,
    'declaration-block-no-redundant-longhand-properties': null,
    
    // Permitir valores calc() sin espacios
    'function-calc-no-unspaced-operator': true,
    
    // Flexibilidad con colores
    'color-hex-length': null,
    'color-named': null,
    
    // Permitir !important cuando sea necesario
    'declaration-no-important': null,
    
    // Flexibilidad con selectores
    'selector-id-pattern': null,
    'selector-nested-pattern': null,
    
    // Flexibilidad con keyframes (permitir camelCase)
    'keyframes-name-pattern': null,
    
    // Flexibilidad con media queries (permitir notación antigua)
    'media-feature-range-notation': null,
    
    // Flexibilidad con orden de especificidad
    'no-descending-specificity': null,
    
    // Flexibilidad con valores shorthand redundantes
    'shorthand-property-no-redundant-values': null,
    
    // Flexibilidad con líneas vacías antes de reglas
    'rule-empty-line-before': null,
    
    // Permitir propiedades deprecadas (word-wrap -> overflow-wrap)
    'property-no-deprecated': null,
    
    // Permitir selectores duplicados (a veces necesario en Vue con scoped)
    'no-duplicate-selectors': null,
    
    // Flexibilidad con comillas en nombres de fuentes
    'font-family-name-quotes': null,
  },
  ignoreFiles: [
    'node_modules/**',
    'dist/**',
    'coverage/**',
    '**/*.d.ts',
    '**/assets/**',
  ],
};

