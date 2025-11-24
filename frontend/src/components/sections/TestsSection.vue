<template>
  <div class="tests-section">
    <h2 class="section-title">{{ $t('tests.title') }}</h2>
    <div class="tests-grid">
      <p class="empty-state">{{ $t('tests.empty') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
.tests-section {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;

  .section-title {
    font-size: 2rem;
    color: var(--accent);
    margin-bottom: 24px;
  }

  .tests-grid {
    display: grid;
    gap: 24px;
  }

  .empty-state {
    text-align: center;
    padding: 40px 20px;
    color: var(--muted);
    font-size: 1rem;
  }
}

@media (max-width: 768px) {
  .tests-section {
    padding: 16px;

    .section-title {
      font-size: 1.5rem;
    }
  }
}
</style>
