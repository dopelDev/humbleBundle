<template>
  <div
    v-if="books && books.length > 0"
    class="books-preview"
    :class="{ expanded: isExpanded }"
    @click.stop="$emit('toggle')"
  >
    <div
      v-for="(book, idx) in displayedBooks"
      :key="book.machine_name || idx"
      class="book-preview-item"
    >
      {{ book.title || book.machine_name }}
    </div>
    <div
      v-if="books.length > previewLimit && !isExpanded"
      class="more-books clickable"
    >
      +{{ books.length - previewLimit }} {{ $t('bundlesUtility.bundle.moreBooks') }}
    </div>
    <div
      v-if="isExpanded && books.length > previewLimit"
      class="more-books clickable"
    >
      {{ $t('bundlesUtility.bundle.collapseBooks') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { BookItem } from '@/types/bundle';

interface Props {
  books?: BookItem[];
  isExpanded?: boolean;
  previewLimit?: number;
}

const props = withDefaults(defineProps<Props>(), {
  books: () => [],
  isExpanded: false,
  previewLimit: 5,
});

defineEmits<{
  toggle: [];
}>();

const displayedBooks = computed(() => {
  if (props.isExpanded) {
    return props.books;
  }
  return props.books.slice(0, props.previewLimit);
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.books-preview {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 8px;
  max-height: 200px;
  overflow-y: auto;
  padding: 8px;
  background: var(--background);
  border-radius: 6px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--accent);
    opacity: 0.95;
  }

  &.expanded {
    max-height: 500px;
  }

  .book-preview-item {
    padding: 4px 0;
    font-size: 0.85rem;
    color: var(--text);
    border-bottom: 1px dashed var(--border);

    &:last-child {
      border-bottom: none;
    }
  }

  .more-books {
    padding: 8px 0;
    font-size: 0.85rem;
    color: var(--accent);
    font-weight: 600;
    text-align: center;

    &.clickable {
      cursor: pointer;
      transition: color 0.2s;

      &:hover {
        color: var(--button-blue);
      }
    }
  }
}
</style>
