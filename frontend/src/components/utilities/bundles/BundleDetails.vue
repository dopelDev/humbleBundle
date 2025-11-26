<template>
  <div class="bundle-details">
    <div class="details-grid">
      <div class="detail-item">
        <strong>{{ $t('bundlesUtility.bundle.id') }}</strong> {{ props.bundle.id }}
      </div>
      <div class="detail-item">
        <strong>{{ $t('bundlesUtility.bundle.machineName') }}</strong> {{ props.bundle.machine_name }}
      </div>
      <div v-if="props.bundle.product_url" class="detail-item">
        <strong>{{ $t('bundlesUtility.bundle.url') }}</strong>
        <a :href="props.bundle.product_url" target="_blank" rel="noopener">
          {{ props.bundle.product_url }}
        </a>
      </div>
      <div v-if="props.bundle.start_date_datetime" class="detail-item">
        <strong>{{ $t('bundlesUtility.bundle.start') }}</strong> {{ formattedStartDate }}
      </div>
      <div v-if="props.bundle.end_date_datetime" class="detail-item">
        <strong>{{ $t('bundlesUtility.bundle.end') }}</strong> {{ formattedEndDate }}
      </div>
      <div v-if="props.bundle.duration_days" class="detail-item">
        <strong>{{ $t('bundlesUtility.bundle.duration') }}</strong> {{ props.bundle.duration_days }} {{ $t('bundlesUtility.bundle.days') }}
      </div>
      <div v-if="props.bundle.msrp_total" class="detail-item">
        <strong>{{ $t('bundlesUtility.bundle.msrpTotal') }}</strong> ${{ props.bundle.msrp_total.toFixed(2) }}
      </div>
      <div v-if="props.bundle.price_tiers && props.bundle.price_tiers.length > 0" class="detail-item full-width">
        <strong>{{ $t('bundlesUtility.bundle.prices') }}</strong>
        <PriceTiers :tiers="props.bundle.price_tiers" />
      </div>
      <div v-if="props.bundle.book_list && props.bundle.book_list.length > 0" class="detail-item full-width">
        <strong>{{ $t('bundlesUtility.bundle.books') }} ({{ props.bundle.book_list.length }}):</strong>
        <BooksPreview
          :books="props.bundle.book_list"
          :is-expanded="isBooksExpanded"
          @toggle="$emit('toggle-books')"
        />
      </div>
    </div>
    <ActionButtons>
      <ActionButton
        variant="view"
        @click="$emit('view-json')"
      >
        {{ $t('bundlesUtility.bundle.viewJson') }}
      </ActionButton>
      <ActionButton
        variant="download"
        @click="$emit('download-json')"
      >
        {{ $t('bundlesUtility.bundle.downloadJson') }}
      </ActionButton>
    </ActionButtons>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import type { Bundle } from '@/types/bundle';
import { formatDate } from '@/utils/dateFormatter';
import PriceTiers from './PriceTiers.vue';
import BooksPreview from './BooksPreview.vue';
import ActionButtons from '@/components/utilities/ActionButtons.vue';
import ActionButton from '@/components/utilities/ActionButton.vue';

interface Props {
  bundle: Bundle;
  isBooksExpanded?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  isBooksExpanded: false,
});

const { locale } = useI18n();

defineEmits<{
  'toggle-books': [];
  'view-json': [];
  'download-json': [];
}>();

const formattedStartDate = computed(() => {
  return props.bundle.start_date_datetime
    ? formatDate(props.bundle.start_date_datetime, { locale: locale.value })
    : '';
});

const formattedEndDate = computed(() => {
  return props.bundle.end_date_datetime
    ? formatDate(props.bundle.end_date_datetime, { locale: locale.value })
    : '';
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.bundle-details {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border);

  .details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 12px;
    margin-bottom: 16px;

    .detail-item {
      font-size: 0.9rem;
      color: var(--text);

      strong {
        color: var(--accent);
        margin-right: 8px;
      }

      a {
        color: var(--button-blue);
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }

      &.full-width {
        grid-column: 1 / -1;
      }
    }
  }
}
</style>
