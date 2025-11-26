<template>
  <div
    class="bundle-item"
    :class="{ active: bundle.is_active, inactive: !bundle.is_active }"
  >
    <div class="bundle-header" @click="$emit('toggle')">
      <div class="bundle-info">
        <h4 class="bundle-name">
          {{ bundle.tile_short_name || bundle.tile_name || bundle.machine_name }}
        </h4>
        <div class="bundle-meta">
          <span v-if="bundle.is_active" class="bundle-status active">
            {{ $t('bundlesUtility.bundle.active') }}
          </span>
          <span v-else class="bundle-status inactive">
            {{ $t('bundlesUtility.bundle.inactive') }}
          </span>
          <span v-if="bundle.verification_date" class="bundle-date">
            📅 {{ formattedVerificationDate }}
          </span>
        </div>
      </div>
      <button class="expand-btn" :aria-expanded="isExpanded">
        <span class="expand-icon">{{ isExpanded ? '−' : '+' }}</span>
      </button>
    </div>

    <div v-show="isExpanded" class="bundle-details-wrapper">
      <BundleDetails
        :bundle="bundle"
        :is-books-expanded="isBooksExpanded"
        @toggle-books="$emit('toggle-books')"
        @view-json="$emit('view-json')"
        @download-json="$emit('download-json')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import type { Bundle } from '@/types/bundle';
import { formatDate } from '@/utils/dateFormatter';
import BundleDetails from './BundleDetails.vue';

interface Props {
  bundle: Bundle;
  isExpanded?: boolean;
  isBooksExpanded?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  isExpanded: false,
  isBooksExpanded: false,
});

const { locale } = useI18n();

defineEmits<{
  toggle: [];
  'toggle-books': [];
  'view-json': [];
  'download-json': [];
}>();

const formattedVerificationDate = computed(() => {
  return props.bundle.verification_date
    ? formatDate(props.bundle.verification_date, { locale: locale.value })
    : '';
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.bundle-item {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px var(--shadow-black-light);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px var(--shadow-black);
  }

  &.active {
    border-left: 4px solid var(--button-green);
  }

  &.inactive {
    border-left: 4px solid var(--text);
    opacity: 0.8;
  }

  .bundle-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    cursor: pointer;
    gap: 16px;

    .bundle-info {
      flex: 1;

      .bundle-name {
        font-size: 1.2rem;
        color: var(--accent);
        margin: 0 0 8px 0;
        font-weight: 600;
      }

      .bundle-meta {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        font-size: 0.85rem;
        color: var(--text);
        opacity: 0.8;

        .bundle-status,
        .bundle-date {
          display: inline-flex;
          align-items: center;
          gap: 4px;
        }

        .bundle-status {
          &.active {
            color: var(--button-green);
          }

          &.inactive {
            color: var(--text);
            opacity: 0.6;
          }
        }
      }
    }

    .expand-btn {
      background: transparent;
      border: 1px solid var(--border);
      border-radius: 6px;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text);
      transition: all 0.2s;

      &:hover {
        background: var(--background);
        border-color: var(--accent);
      }

      .expand-icon {
        font-size: 1.2rem;
        font-weight: 700;
      }
    }
  }

  .bundle-details-wrapper {
    margin-top: 16px;
  }

  @media (max-width: 768px) {
    .bundle-header {
      flex-direction: column;
      gap: 12px;

      .expand-btn {
        align-self: flex-end;
      }
    }
  }
}
</style>
