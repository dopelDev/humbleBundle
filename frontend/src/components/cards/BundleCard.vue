<template>
  <article class="bundle-card" :id="`bundle-${bundle.id}`" @click="openModal">
    <div class="bundle-image-wrapper" v-if="bundle.tile_logo || bundle.featured_image">
      <img
        v-if="bundle.tile_logo"
        :src="getImageUrl(bundle.tile_logo)"
        :alt="bundle.tile_short_name ?? bundle.tile_name"
        loading="lazy"
        @error="handleImageError"
        class="bundle-logo"
      />
      <img
        v-else-if="bundle.featured_image"
        :src="getImageUrl(bundle.featured_image)"
        :alt="bundle.tile_short_name ?? bundle.tile_name"
        loading="lazy"
        @error="handleImageError"
        class="bundle-image"
      />
    </div>
    <div class="bundle-content">
      <h3>{{ bundle.tile_short_name ?? bundle.tile_name }}</h3>
      <p class="meta">
        {{ bundle.category }} • {{ $t('bundleCard.ends') }} {{
          formatDate(bundle.end_date_datetime)
        }}
      </p>
      <p class="msrp">MSRP: ${{ bundle.msrp_total ?? "—" }}</p>
      <div class="tiers" v-if="bundle.price_tiers?.length">
        <span v-for="tier in bundle.price_tiers.slice(0, 2)" :key="tier.identifier">
          {{ tier.header }}
        </span>
      </div>
      <a class="link" :href="bundle.product_url" target="_blank" rel="noopener" @click.stop>
        {{ $t('bundleCard.viewBundle') }}
      </a>
    </div>
  </article>

  <Teleport to="body">
    <BookModal
      v-if="showModal"
      :bundle="bundle"
      @close="closeModal"
    />
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import type { Bundle } from "@/types/bundle";
import BookModal from "./BookModal.vue";

defineProps<{ bundle: Bundle }>();

const { locale } = useI18n();
const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const formatDate = (value?: string) => {
  if (!value) return "—";
  const dateLocale = locale.value === 'es' ? 'es-PE' : 'en-US';
  return new Date(value).toLocaleDateString(dateLocale, {
    month: "short",
    day: "numeric"
  });
};

// Obtener URL de imagen directamente desde Humble Bundle
// Las imágenes se extraen SOLO de divs con clase "img-container"
const getImageUrl = (imageUrl: string | null | undefined): string => {
  if (!imageUrl) return '';
  return imageUrl;
};

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  img.style.display = 'none';
  console.warn('Error cargando imagen del bundle:', img.src);
};
</script>

<style scoped lang="scss">
.bundle-card {
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;

  &:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 24px var(--shadow-black-medium);
  }

  .bundle-image-wrapper {
    width: 100%;
    height: 200px;
    overflow: hidden;
    background: var(--surface);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .bundle-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .bundle-logo {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 20px;
  }

  .bundle-content {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
  }

  h3 {
    font-size: 1.1rem;
    color: var(--accent);
    margin: 0;
  }

  .meta {
    font-size: 0.85rem;
    color: var(--text);
    margin: 0;
  }

  .msrp {
    font-weight: 600;
    color: var(--primary);
    margin: 0;
  }

  .tiers {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;

    span {
      background: var(--surface);
      color: var(--accent);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.75rem;
    }
  }

  .link {
    margin-top: auto;
    font-weight: 600;
    color: var(--accent);
  }
}
</style>

