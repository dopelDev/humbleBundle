<template>
  <div class="filters-section">
    <div class="filter-group">
      <label v-if="label" class="filter-label">{{ label }}</label>
      <select
        :model-value="modelValue"
        @update:model-value="$emit('update:modelValue', $event)"
        class="filter-select"
      >
        <option
          v-for="option in options"
          :key="option.value"
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>
    </div>
    <BaseButton
      :variant="refreshButtonVariant"
      :disabled="loading"
      @click="$emit('refresh')"
    >
      {{ loading ? loadingText : refreshText }}
    </BaseButton>
  </div>
</template>

<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue';

interface FilterOption {
  value: string;
  label: string;
}

interface Props {
  modelValue: string;
  options: FilterOption[];
  label?: string;
  loading?: boolean;
  refreshText?: string;
  loadingText?: string;
  refreshButtonVariant?: 'primary' | 'secondary' | 'accent' | 'blue' | 'green' | 'transparent';
}

withDefaults(defineProps<Props>(), {
  label: '',
  loading: false,
  refreshText: 'Actualizar',
  loadingText: 'Cargando...',
  refreshButtonVariant: 'accent',
});

defineEmits<{
  'update:modelValue': [value: string];
  refresh: [];
}>();
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.filters-section {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
  padding: 16px;
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 8px;

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 8px;

    .filter-label {
      font-size: 0.9rem;
      color: var(--text);
      font-weight: 600;
    }

    .filter-select {
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      font-size: 0.9rem;
      cursor: pointer;
      min-width: 150px;

      &:focus {
        outline: none;
        border-color: var(--accent);
      }
    }
  }

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;

    .filter-group {
      width: 100%;

      .filter-select {
        width: 100%;
      }
    }
  }
}
</style>
