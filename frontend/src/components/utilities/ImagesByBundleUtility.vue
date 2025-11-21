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
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;

  .utility-title {
    font-size: 1.5rem;
    color: var(--accent);
    margin: 0 0 12px 0;
  }

  .utility-description {
    color: var(--text);
    margin: 0 0 24px 0;
    opacity: 0.9;
  }
}

@media (max-width: 768px) {
  .utility-card {
    padding: 16px;
  }
}
</style>
