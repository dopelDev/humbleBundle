<template>
  <div class="test-card">
    <div class="test-header">
      <h3 class="test-title">Test Card</h3>
    </div>
    <p class="test-description">Test description placeholder</p>
  </div>
</template>

<script setup lang="ts">
// Stub component - diseño mantenido para uso futuro
</script>

<style scoped lang="scss">
.test-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  transition: box-shadow 0.2s ease;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}

.test-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  gap: 16px;
}

.test-title {
  font-size: 1.25rem;
  color: var(--accent);
  margin: 0;
  flex: 1;
}

.test-description {
  color: var(--text);
  margin: 0 0 16px 0;
  line-height: 1.6;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .test-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
