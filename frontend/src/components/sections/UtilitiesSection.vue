<template>
  <div class="utilities-section">
    <h2 class="section-title">Utilidades</h2>
    
    <LandingPageRawDataUtility />
  </div>
</template>

<script setup lang="ts">
import LandingPageRawDataUtility from "@/components/sections/utilities/LandingPageRawDataUtility.vue";
</script>

<style scoped lang="scss">
.utilities-section {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
  border-top: 1px solid var(--border);
  margin-top: 48px;
  padding-top: 48px;

  .section-title {
    font-size: 2rem;
    color: var(--accent);
    margin-bottom: 24px;
  }
}

@media (max-width: 768px) {
  .utilities-section {
    padding: 16px;
    margin-top: 32px;
    padding-top: 32px;

    .section-title {
      font-size: 1.5rem;
    }
  }
}
</style>
