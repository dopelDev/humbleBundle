<template>
  <div class="records-list">
    <RawDataRecordItem
      v-for="record in records"
      :key="record.id"
      :record="record"
      @select="$emit('select', record)"
      @view-json="$emit('view-json', record)"
      @download-json="$emit('download-json', record)"
    />
  </div>
</template>

<script setup lang="ts">
import type { LandingPageRawData } from '@/types/rawData';
import RawDataRecordItem from './RawDataRecordItem.vue';

interface Props {
  records: LandingPageRawData[];
}

defineProps<Props>();

defineEmits<{
  select: [record: LandingPageRawData];
  'view-json': [record: LandingPageRawData];
  'download-json': [record: LandingPageRawData];
}>();
</script>

<style scoped lang="scss">
.records-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  padding: 4px;
}
</style>
