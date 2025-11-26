<template>
  <div v-if="message" class="error-message">
    <slot>
      {{ message }}
    </slot>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message?: string;
}

withDefaults(defineProps<Props>(), {
  message: '',
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.error-message {
  background: var(--error-bg);
  border: 1px solid var(--error-border);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: var(--error-red);
  font-size: 0.9rem;
}
</style>
