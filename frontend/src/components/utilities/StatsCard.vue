<template>
  <div class="stat-card">
    <div class="stat-value">{{ value }}</div>
    <div class="stat-label">{{ label }}</div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  value: string | number;
  label: string;
}

defineProps<Props>();
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.stat-card {
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  text-align: center;

  .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 4px;
  }

  .stat-label {
    font-size: 0.9rem;
    color: var(--text);
    opacity: 0.8;
  }
}
</style>
