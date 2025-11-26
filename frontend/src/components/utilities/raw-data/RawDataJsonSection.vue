<template>
  <div v-if="record || isLoading" class="json-section">
    <div class="json-header">
      <h4>{{ $t('rawDataUtility.jsonData') }}</h4>
    </div>
    <div v-show="isLoading" class="detail-loading">
      {{ $t('rawDataUtility.loadingDetail') }}
    </div>
    <div v-if="record">
      <div class="json-meta">
        <div class="meta-item">
          <strong>{{ $t('rawDataUtility.date') }}</strong> {{ formattedDate }}
        </div>
        <div class="meta-item">
          <strong>{{ $t('rawDataUtility.url') }}</strong> {{ record.source_url }}
        </div>
        <div v-if="record.json_hash" class="meta-item">
          <strong>{{ $t('rawDataUtility.hash') }}</strong> {{ record.json_hash }}
        </div>
        <div class="meta-item">
          <strong>{{ $t('rawDataUtility.size') }}</strong> {{ formattedSize }}
        </div>
      </div>
      <ActionButtons>
        <ActionButton
          variant="view"
          @click="$emit('view-json')"
        >
          {{ $t('rawDataUtility.viewJson') }}
        </ActionButton>
        <ActionButton
          variant="download"
          @click="$emit('download-json')"
        >
          {{ $t('rawDataUtility.downloadJson') }}
        </ActionButton>
      </ActionButtons>
    </div>
    <div v-else class="detail-loading">
      {{ $t('rawDataUtility.selectRecord') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import type { LandingPageRawData } from '@/types/rawData';
import { formatDate } from '@/utils/dateFormatter';
import { formatJsonSize } from '@/utils/sizeFormatter';
import ActionButtons from '@/components/utilities/ActionButtons.vue';
import ActionButton from '@/components/utilities/ActionButton.vue';

interface Props {
  record: LandingPageRawData | null;
  isLoading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  record: null,
  isLoading: false,
});

const { locale } = useI18n();

defineEmits<{
  'view-json': [];
  'download-json': [];
}>();

const formattedDate = computed(() => {
  return props.record
    ? formatDate(props.record.scraped_date, {
        includeSeconds: true,
        locale: locale.value,
      })
    : '';
});

const formattedSize = computed(() => {
  if (!props.record) return '';
  const jsonString = JSON.stringify(props.record.json_data, null, 2);
  return formatJsonSize(jsonString);
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.json-section {
  h4 {
    font-size: 1.1rem;
    color: var(--accent);
    margin: 0 0 16px 0;
  }

  .json-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    @media (max-width: 768px) {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
    }
  }

  .json-meta {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 16px;
    font-size: 0.9rem;

    .meta-item {
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }

      strong {
        color: var(--accent);
        margin-right: 8px;
      }
    }
  }

  .detail-loading {
    margin-bottom: 8px;
    color: var(--text);
    opacity: 0.8;
    font-size: 0.9rem;
  }
}
</style>
