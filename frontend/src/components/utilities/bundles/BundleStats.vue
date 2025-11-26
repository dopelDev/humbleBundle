<template>
  <StatsSection>
    <StatsCard
      :value="totalBundles"
      :label="$t('bundlesUtility.stats.totalBundles')"
    />
    <StatsCard
      :value="activeBundles"
      :label="$t('bundlesUtility.stats.active')"
    />
    <StatsCard
      :value="inactiveBundles"
      :label="$t('bundlesUtility.stats.inactive')"
    />
  </StatsSection>
</template>

<script setup lang="ts">
import StatsSection from '@/components/utilities/StatsSection.vue';
import StatsCard from '@/components/utilities/StatsCard.vue';

interface Props {
  totalBundles: number;
  activeBundles: number;
  inactiveBundles: number;
}

defineProps<Props>();
</script>
