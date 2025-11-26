<template>
  <button
    :class="buttonClass"
    :disabled="disabled"
    :type="type"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'accent' | 'blue' | 'green' | 'transparent';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'medium',
  disabled: false,
  type: 'button',
});

defineEmits<{
  click: [event: MouseEvent];
}>();

const buttonClass = computed(() => ({
	'base-button': true,
  [`variant-${props.variant}`]: true,
  [`size-${props.size}`]: true,
  disabled: props.disabled,
}));
</script>

<script lang="ts">
import { computed } from 'vue';
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.base-button {
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;

  &.size-small {
    padding: 6px 12px;
    font-size: 0.85rem;
  }

  &.size-medium {
    padding: 8px 16px;
    font-size: 0.9rem;
  }

  &.size-large {
    padding: 12px 24px;
    font-size: 1rem;
  }

  &.variant-primary {
    background: var(--primary);
    color: white;

    &:hover:not(.disabled) {
      opacity: 0.9;
    }
  }

  &.variant-accent {
    background: var(--accent);
    color: white;

    &:hover:not(.disabled) {
      opacity: 0.9;
    }
  }

  &.variant-blue {
    background: var(--button-blue);
    color: white;

    &:hover:not(.disabled) {
      opacity: 0.9;
      transform: translateY(-1px);
    }
  }

  &.variant-green {
    background: var(--button-green);
    color: white;

    &:hover:not(.disabled) {
      opacity: 0.9;
      transform: translateY(-1px);
    }
  }

  &.variant-secondary {
    background: var(--background);
    color: var(--text);
    border: 1px solid var(--border);

    &:hover:not(.disabled) {
      background: var(--surface);
      border-color: var(--accent);
    }
  }

  &.variant-transparent {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);

    &:hover:not(.disabled) {
      background: var(--background);
      border-color: var(--accent);
    }
  }

  &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>
