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
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 600px;
  overflow-y: auto;
  padding: 4px;
}
</style>
