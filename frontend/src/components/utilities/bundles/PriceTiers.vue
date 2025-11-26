<template>
  <div v-if="tiers && tiers.length > 0" class="price-tiers">
    <div
      v-for="(tier, idx) in tiers"
      :key="idx"
      class="price-tier"
    >
      <span class="tier-name">{{ tier.header || tier.identifier }}</span>
      <span v-if="tier.price" class="tier-price">
        {{ tier.price.currency }} {{ tier.price.amount }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PriceTier } from '@/types/bundle';

interface Props {
  tiers?: PriceTier[];
}

defineProps<Props>();
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.price-tiers {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;

  .price-tier {
    display: flex;
    justify-content: space-between;
    padding: 8px;
    background: var(--background);
    border-radius: 6px;
    border: 1px solid var(--border);

    .tier-name {
      font-weight: 600;
    }

    .tier-price {
      color: var(--accent);
      font-weight: 600;
    }
  }
}
</style>
