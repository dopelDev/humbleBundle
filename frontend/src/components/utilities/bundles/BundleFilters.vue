<template>
  <FilterSection
    :model-value="modelValue"
    :options="filterOptions"
    :label="$t('bundlesUtility.filters.status')"
    :loading="loading"
    :refresh-text="$t('bundlesUtility.buttons.update')"
    :loading-text="$t('bundlesUtility.buttons.loading')"
    @update:model-value="handleUpdate"
    @refresh="$emit('refresh')"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import FilterSection from '@/components/utilities/FilterSection.vue';

interface Props {
  modelValue: 'all' | 'active' | 'inactive';
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
});

const { t } = useI18n();

const emit = defineEmits<{
  'update:modelValue': [value: 'all' | 'active' | 'inactive'];
  refresh: [];
}>();

const filterOptions = computed(() => [
  { value: 'all', label: t('bundlesUtility.filters.all') },
  { value: 'active', label: t('bundlesUtility.filters.active') },
  { value: 'inactive', label: t('bundlesUtility.filters.inactive') },
]);

function handleUpdate(value: string) {
  if (value === 'all' || value === 'active' || value === 'inactive') {
    emit('update:modelValue', value);
  }
}
</script>
