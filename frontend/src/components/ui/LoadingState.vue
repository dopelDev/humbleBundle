<template>
  <div class="loading-state">
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

.loading-state {
  text-align: center;
  padding: 24px;
  color: var(--text);
  opacity: 0.7;
  font-size: 0.9rem;
}
</style>
