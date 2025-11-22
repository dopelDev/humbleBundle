<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ bundle.tile_short_name ?? bundle.tile_name }}</h2>
        <button class="close-btn" @click="$emit('close')" aria-label="Cerrar">
          ×
        </button>
      </div>

      <div v-if="bundle.featured_image" class="bundle-image-section">
        <div class="bundle-image-wrapper">
          <img 
            :src="getImageUrl(bundle.featured_image)" 
            :alt="bundle.tile_name || 'Bundle image'" 
            class="bundle-image"
          />
        </div>
      </div>

      <div class="modal-body">
        <div v-if="bundle.book_list && bundle.book_list.length > 0" class="books-list">
          <div
            v-for="book in bundle.book_list"
            :key="book.machine_name"
            class="book-item"
            :class="{ expanded: expandedBooks.has(book.machine_name) }"
          >
            <div class="book-info" @click="toggleBook(book.machine_name)">
              <div class="book-header">
                <div class="book-image-wrapper" v-if="book.image">
                  <img :src="getImageUrl(book.image)" :alt="book.title || 'Book cover'" class="book-image" />
                </div>
                <div class="book-image-placeholder" v-else>
                  <span class="placeholder-icon">📖</span>
                </div>
                <h4 class="book-title">{{ book.title }}</h4>
              </div>
              <button class="expand-btn" :aria-expanded="expandedBooks.has(book.machine_name)">
                <span class="expand-icon">{{ expandedBooks.has(book.machine_name) ? '−' : '+' }}</span>
              </button>
            </div>
            <div
              v-show="expandedBooks.has(book.machine_name) && book.image"
              class="book-expanded-image"
            >
              <img :src="getImageUrl(book.image)" :alt="book.title || 'Book cover'" class="expanded-book-image" />
            </div>
          </div>
        </div>
        <div v-else class="no-books">
          <p>No hay libros disponibles para este bundle.</p>
        </div>
      </div>

      <div class="modal-footer">
        <a
          class="bundle-link"
          :href="bundle.product_url"
          target="_blank"
          rel="noopener"
        >
          Ver bundle en Humble →
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { Bundle } from "@/types/bundle";

defineProps<{
  bundle: Bundle;
}>();

const emit = defineEmits<{
  close: [];
}>();

const expandedBooks = ref<Set<string>>(new Set());

const toggleBook = (machineName: string) => {
  if (expandedBooks.value.has(machineName)) {
    expandedBooks.value.delete(machineName);
  } else {
    expandedBooks.value.add(machineName);
  }
};

// Obtener URL de imagen directamente desde Humble Bundle
// Las URLs vienen completas desde el backend, no necesitan construcción adicional
const getImageUrl = (imageUrl: string | null | undefined): string => {
  if (!imageUrl) return '';
  
  // Las URLs del backend son absolutas (https://www.humblebundle.com/... o https://hb.imgix.net/...)
  // Solo retornamos la URL tal cual
  return imageUrl;
};

const handleOverlayClick = (event: MouseEvent) => {
  if (event.target === event.currentTarget) {
    emit("close");
  }
};
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  inset: 0;
  background: var(--overlay-black);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 20px;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: var(--bg);
  border-radius: 24px;
  max-width: 700px;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px var(--shadow-black-dark);
  border: 1px solid var(--border);
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid var(--border);

  h2 {
    font-size: 1.5rem;
    color: var(--accent);
    margin: 0;
  }

  .close-btn {
    background: transparent;
    border: none;
    font-size: 2rem;
    color: var(--text);
    cursor: pointer;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background 0.2s ease;

    &:hover {
      background: var(--surface);
    }
  }
}

.bundle-image-section {
  width: 100%;
  padding: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--background);
}

.bundle-image-wrapper {
  width: 100%;
  max-width: 400px;
  background: var(--image-bg);
  border-radius: 16px;
  padding: 16px;
  border: 1px solid var(--border);
  box-shadow: 0 4px 12px var(--shadow-black);
  display: flex;
  justify-content: center;
  align-items: center;
}

// En modo oscuro, usar un fondo más oscuro
:global(body.dark) .bundle-image-wrapper,
:global(body[data-theme="dark"]) .bundle-image-wrapper {
  background: var(--image-bg);
}

.bundle-image {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.books-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.book-item {
  padding: 16px;
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border);
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--primary);
  }

  &.expanded {
    background: var(--bg);
    border-color: var(--primary);
  }
}

.book-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  cursor: pointer;
}

.book-header {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  min-width: 0;
}

.book-image-wrapper {
  flex-shrink: 0;
  width: 60px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg);
  border: 1px solid var(--border);
}

.book-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-image-placeholder {
  flex-shrink: 0;
  width: 60px;
  height: 80px;
  border-radius: 8px;
  background: var(--bg);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.book-title {
  font-size: 1rem;
  color: var(--text);
  margin: 0;
  flex: 1;
  min-width: 0;
  word-wrap: break-word;
}

.expand-btn {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
  color: var(--text);

  &:hover {
    background: var(--surface);
    border-color: var(--primary);
  }

  .expand-icon {
    font-size: 1.2rem;
    font-weight: bold;
    line-height: 1;
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 500px;
  }
}

.book-title {
  font-size: 1rem;
  color: var(--text);
  margin: 0;
  flex: 1;
  min-width: 200px;
}

.book-expanded-image {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: center;
  animation: slideDown 0.3s ease;
}

.expanded-book-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 12px;
  box-shadow: 0 4px 12px var(--shadow-black-medium);
  object-fit: contain;
}

.no-books {
  text-align: center;
  padding: 40px 20px;
  color: var(--muted);

  p {
    margin: 0;
  }
}

.modal-footer {
  padding: 24px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: center;
}

.bundle-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;

  &:hover {
    color: var(--primary);
  }
}

@media (max-width: 768px) {
  .modal-content {
    max-height: 90vh;
    border-radius: 16px;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 16px;
  }

  .bundle-image-section {
    padding: 16px;
  }

  .bundle-image-wrapper {
    max-width: 100%;
    padding: 12px;
  }

  .bundle-image {
    max-height: 200px;
  }

  .book-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .book-title {
    min-width: auto;
  }
}
</style>

