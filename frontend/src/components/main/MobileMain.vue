<template>
  <main class="mobile-main">
    <FeaturedBundle :bundle="featured" />
    <section id="bundles">
      <h2>{{ $t('main.bundles') }}</h2>
      <div class="stack">
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
.mobile-main {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;

  .stack {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
}
</style>

