<template>
  <main class="desktop-main">
    <FeaturedBundle :bundle="featured" />

    <section id="bundles" class="grid">
      <h2>Bundles activos</h2>
      <div class="grid-list">
        <BundleCard v-for="bundle in bundles" :key="bundle.id" :bundle="bundle" />
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import type { Bundle } from "@/types/bundle";
import FeaturedBundle from "@components/cards/FeaturedBundle.vue";
import BundleCard from "@components/cards/BundleCard.vue";

defineProps<{
  bundles: Bundle[];
  featured: Bundle | null;
}>();
</script>

<style scoped lang="scss">
.desktop-main {
  display: flex;
  flex-direction: column;
  gap: 48px;
  padding: 32px 64px 64px;
}

.grid {
  display: flex;
  flex-direction: column;
  gap: 24px;

  .grid-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 1024px) {
  .desktop-main {
    padding: 24px;
  }
}
</style>

