<template>
  <div class="utility-card">
    <h3 class="utility-title">Utility Card</h3>
    <p class="utility-description">
      Utility description placeholder
    </p>
  </div>
</template>

<script setup lang="ts">
// Stub component - diseño mantenido para uso futuro
</script>

<style scoped lang="scss">
.utility-card {
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

.utility-title {
  font-size: 1.25rem;
  color: var(--accent);
  margin: 0 0 12px 0;
}

.utility-description {
  color: var(--text);
  margin: 0;
  line-height: 1.6;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .utility-card {
    padding: 16px;
  }
}
</style>
