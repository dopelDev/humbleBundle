<template>
  <div class="record-item" @click="$emit('select')">
    <div class="record-content">
      <div class="record-header">
        <div class="record-date-section">
          <span class="record-label">{{ $t('rawDataUtility.date') }}</span>
          <span class="record-date">{{ formattedDate }}</span>
        </div>
        <div v-if="record.json_hash" class="record-hash-section">
          <span class="record-label">{{ $t('rawDataUtility.hash') }}</span>
          <span class="record-hash" :title="record.json_hash">
            {{ record.json_hash.substring(0, 12) }}...
          </span>
        </div>
      </div>
      <div class="record-meta">
        <span class="record-label">{{ $t('rawDataUtility.url') }}</span>
        <span class="record-source">{{ record.source_url }}</span>
      </div>
      <div v-if="record.json_version" class="record-version">
        <span class="record-label">{{ $t('rawDataUtility.version') }}</span>
        <span>{{ record.json_version }}</span>
      </div>
      <ActionButtons>
        <ActionButton
          variant="view"
          @click.stop="$emit('view-json')"
        >
          {{ $t('rawDataUtility.viewJson') }}
        </ActionButton>
        <ActionButton
          variant="download"
          @click.stop="$emit('download-json')"
        >
          {{ $t('rawDataUtility.downloadJson') }}
        </ActionButton>
      </ActionButtons>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import type { LandingPageRawData } from '@/types/rawData';
import { formatDate } from '@/utils/dateFormatter';
import ActionButtons from '@/components/utilities/ActionButtons.vue';
import ActionButton from '@/components/utilities/ActionButton.vue';

interface Props {
  record: LandingPageRawData;
}

const props = defineProps<Props>();

const { locale } = useI18n();

defineEmits<{
  select: [];
  'view-json': [];
  'download-json': [];
}>();

const formattedDate = computed(() => {
  return formatDate(props.record.scraped_date, {
    includeSeconds: true,
    locale: locale.value,
  });
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.record-item {
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  transition: all 0.2s ease;
  overflow: hidden;
  cursor: pointer;

  &:hover {
    border-color: var(--accent);
    box-shadow: 0 2px 8px var(--shadow-black-light);
  }

  .record-content {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .record-header {
    display: flex;
    flex-direction: column;
    gap: 8px;

    .record-date-section,
    .record-hash-section {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .record-label {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent);
      min-width: 60px;
    }

    .record-date {
      font-weight: 600;
      font-size: 0.95rem;
      color: var(--text);
    }

    .record-hash {
      font-family: monospace;
      font-size: 0.85rem;
      color: var(--text);
      opacity: 0.9;
      word-break: break-all;
    }
  }

  .record-meta {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 0.9rem;

    .record-label {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent);
      min-width: 60px;
      flex-shrink: 0;
    }

    .record-source {
      word-break: break-all;
      color: var(--text);
      opacity: 0.9;
      flex: 1;
    }
  }

  .record-version {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: var(--text);
    opacity: 0.8;

    .record-label {
      font-weight: 600;
      color: var(--accent);
      min-width: 60px;
    }
  }
}
</style>
