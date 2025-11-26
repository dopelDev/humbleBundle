<template>
  <div class="base-card" :class="cardClass">
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'default' | 'surface' | 'background';
  padding?: 'none' | 'small' | 'medium' | 'large';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  padding: 'medium',
});

const cardClass = computed(() => ({
  [`variant-${props.variant}`]: true,
  [`padding-${props.padding}`]: true,
}));
</script>

<script lang="ts">
import { computed } from 'vue';
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.base-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  transition: all 0.2s ease;

  &.variant-default {
    background: var(--surface);
  }

  &.variant-surface {
    background: var(--surface);
  }

  &.variant-background {
    background: var(--background);
  }

  &.padding-none {
    padding: 0;
  }

  &.padding-small {
    padding: 12px;
  }

  &.padding-medium {
    padding: 24px;
  }

  &.padding-large {
    padding: 32px;
  }
}
</style>
