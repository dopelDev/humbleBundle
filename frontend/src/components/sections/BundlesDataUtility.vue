<template>
  <BaseCard class="utility-card">
    <h3 class="utility-title">{{ $t('bundlesUtility.title') }}</h3>
    <p class="utility-description">
      {{ $t('bundlesUtility.description') }}
    </p>

    <ErrorMessage :message="error ?? undefined" />

    <LoadingState v-show="loading" :message="$t('bundlesUtility.loading')" />

    <div v-if="!loading && !error" class="bundles-container">
      <BundleStats
        :total-bundles="bundles.length"
        :active-bundles="activeBundles.length"
        :inactive-bundles="inactiveBundles.length"
      />

      <BundleFilters
        v-model="statusFilter"
        :loading="loading"
        @refresh="loadData"
      />

      <div class="bundles-list">
        <EmptyState
          v-if="filteredBundles.length === 0"
          :message="$t('bundlesUtility.emptyState')"
        />

        <BundleListItem
          v-for="bundle in filteredBundles"
          :key="bundle.id"
          :bundle="bundle"
          :is-expanded="expandedBundles === bundle.id"
          :is-books-expanded="expandedBooks.has(bundle.id)"
          @toggle="toggleBundle(bundle.id)"
          @toggle-books="toggleBooks(bundle.id)"
          @view-json="viewBundleJson(bundle)"
          @download-json="downloadBundleJson(bundle)"
        />
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useBundles } from '@/composables/useBundles';
import type { Bundle } from '@/types/bundle';
import { viewJson, downloadJson } from '@/utils/jsonHandler';
import BaseCard from '@/components/ui/BaseCard.vue';
import ErrorMessage from '@/components/ui/ErrorMessage.vue';
import LoadingState from '@/components/ui/LoadingState.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import BundleStats from '@/components/utilities/bundles/BundleStats.vue';
import BundleFilters from '@/components/utilities/bundles/BundleFilters.vue';
import BundleListItem from '@/components/utilities/bundles/BundleListItem.vue';

const { bundles, loading, error, refresh } = useBundles();

const statusFilter = ref<'all' | 'active' | 'inactive'>('all');
const expandedBundles = ref<string | null>(null);
const expandedBooks = ref<Set<string>>(new Set());

const activeBundles = computed(() =>
  bundles.value.filter((b) => b.is_active)
);

const inactiveBundles = computed(() =>
  bundles.value.filter((b) => !b.is_active)
);

const filteredBundles = computed(() => {
  let filtered = bundles.value;

  if (statusFilter.value === 'active') {
    filtered = filtered.filter((b) => b.is_active);
  } else if (statusFilter.value === 'inactive') {
    filtered = filtered.filter((b) => !b.is_active);
  }

  return filtered.sort((a, b) => {
    if (a.is_active !== b.is_active) {
      return a.is_active ? -1 : 1;
    }
    const dateA = a.verification_date ? new Date(a.verification_date).getTime() : 0;
    const dateB = b.verification_date ? new Date(b.verification_date).getTime() : 0;
    return dateB - dateA;
  });
});

function toggleBundle(bundleId: string) {
  if (expandedBundles.value === bundleId) {
    expandedBundles.value = null;
    expandedBooks.value.delete(bundleId);
  } else {
    expandedBundles.value = bundleId;
    expandedBooks.value.delete(bundleId);
  }
}

function toggleBooks(bundleId: string) {
  if (expandedBooks.value.has(bundleId)) {
    expandedBooks.value.delete(bundleId);
  } else {
    expandedBooks.value.add(bundleId);
  }
}

function viewBundleJson(bundle: Bundle) {
  viewJson(bundle);
}

function downloadBundleJson(bundle: Bundle) {
  downloadJson(bundle, `bundle-${bundle.machine_name || bundle.id}.json`);
}

function loadData() {
  refresh();
}

onMounted(() => {
  loadData();
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.utility-card {
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

.bundles-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.bundles-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 800px;
  overflow-y: auto;
  padding: 8px;
}

@media (max-width: 768px) {
  .utility-card {
    padding: 16px;
  }
}
</style>
