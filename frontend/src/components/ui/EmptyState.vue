<template>
  <div class="empty-state" :class="`size-${size}`">
    <slot>
      {{ message }}
    </slot>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message?: string;
  size?: 'small' | 'medium' | 'large';
}

withDefaults(defineProps<Props>(), {
  message: '',
  size: 'medium',
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.empty-state {
  text-align: center;
  color: var(--text);
  opacity: 0.7;

  &.size-small {
    padding: 24px;
    font-size: 0.9rem;
  }

  &.size-medium {
    padding: 48px;
    font-size: 1.1rem;
  }

  &.size-large {
    padding: 64px;
    font-size: 1.2rem;
  }
}
</style>
