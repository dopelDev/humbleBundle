<template>
  <BaseCard class="utility-card">
    <h3 class="utility-title">{{ $t('rawDataUtility.title') }}</h3>
    <p class="utility-description">
      {{ $t('rawDataUtility.description') }}
    </p>

    <ErrorMessage :message="error || undefined" />

    <LoadingState v-show="isListLoading" :message="$t('rawDataUtility.loading')" />

    <div class="raw-data-container">
      <div class="records-section">
        <h4>{{ $t('rawDataUtility.storedRecords') }}</h4>
        <BaseButton
          variant="accent"
          :disabled="isListLoading"
          @click="loadData"
        >
          {{ isListLoading ? $t('rawDataUtility.loading') : $t('rawDataUtility.updateList') }}
        </BaseButton>

        <EmptyState
          v-if="rawDataList.length === 0"
          :message="$t('rawDataUtility.emptyState')"
        />

        <RawDataRecordsList
          v-else
          :records="rawDataList"
          @view-json="viewRecordJson"
          @download-json="downloadRecordJson"
        />
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRawData } from '@/composables/useRawData';
import type { LandingPageRawData } from '@/types/rawData';
import { viewJson, downloadJson } from '@/utils/jsonHandler';
import BaseCard from '@/components/ui/BaseCard.vue';
import BaseButton from '@/components/ui/BaseButton.vue';
import ErrorMessage from '@/components/ui/ErrorMessage.vue';
import LoadingState from '@/components/ui/LoadingState.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import RawDataRecordsList from '@/components/utilities/raw-data/RawDataRecordsList.vue';

const {
  rawDataList,
  error,
  fetchRawDataList,
} = useRawData();

const isListLoading = ref(false);

async function loadData() {
  isListLoading.value = true;
  try {
    await fetchRawDataList();
  } finally {
    isListLoading.value = false;
  }
}

function viewRecordJson(record: LandingPageRawData) {
  viewJson(record.json_data);
}

function downloadRecordJson(record: LandingPageRawData) {
  downloadJson(record.json_data, `landing-page-raw-data-${record.id}.json`);
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

.raw-data-container {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.records-section {
  h4 {
    font-size: 1.1rem;
    color: var(--accent);
    margin: 0 0 16px 0;
  }
}

@media (max-width: 768px) {
  .utility-card {
    padding: 16px;	
		right: 16px;
  }

  .raw-data-container {
    gap: 16px;
  }
}
</style>
