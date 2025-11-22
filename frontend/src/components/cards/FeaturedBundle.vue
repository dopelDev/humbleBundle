<template>
  <section id="featured" class="featured" v-if="bundle">
    <div class="hero">
      <img
        v-if="bundle.featured_image"
        :src="getImageUrl(bundle.featured_image)"
        :alt="bundle.tile_name"
        loading="lazy"
      />
      <div class="hero-info">
        <p class="eyebrow">Destacado</p>
        <h2>{{ bundle.tile_name }}</h2>
        <p class="msrp">MSRP estimado: ${{ bundle.msrp_total ?? "—" }}</p>
        <div class="chip-group">
          <span
            v-for="tier in bundle.price_tiers?.slice(0, 3)"
            :key="tier.identifier"
            class="chip"
          >
            {{ tier.header }}
          </span>
        </div>
        <a
          class="cta"
          :href="bundle.product_url"
          target="_blank"
          rel="noopener"
        >
          Ver en Humble →
        </a>
      </div>
    </div>
    <div class="book-preview" v-if="bundle.book_list?.length">
      <h3>Incluye títulos como</h3>
      <ul>
        <li v-for="book in bundle.book_list.slice(0, 6)" :key="book.machine_name">
          {{ book.title }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Bundle } from "@/types/bundle";

defineProps<{
  bundle: Bundle | null;
}>();

// Obtener URL de imagen directamente desde Humble Bundle
// Las URLs vienen completas desde el backend, no necesitan construcción adicional
const getImageUrl = (imageUrl: string | null | undefined): string => {
  if (!imageUrl) return '';
  
  // Las URLs del backend son absolutas (https://www.humblebundle.com/... o https://hb.imgix.net/...)
  // Solo retornamos la URL tal cual
  return imageUrl;
};
</script>

<style scoped lang="scss">
.featured {
  background: linear-gradient(
    135deg,
    var(--gradient-orange),
    var(--gradient-blue)
  );
  border-radius: 24px;
  padding: 32px;
  color: var(--accent);
  display: flex;
  flex-direction: column;
  gap: 24px;

  .hero {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 24px;
    align-items: center;
  }

  img {
    width: 100%;
    border-radius: 16px;
    object-fit: cover;
    box-shadow: 0 12px 24px var(--shadow-black-medium);
  }

  .eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.75rem;
    margin-bottom: 8px;
  }

  h2 {
    font-size: 2rem;
    margin-bottom: 12px;
  }

  .msrp {
    font-size: 1rem;
    color: var(--primary);
  }

  .chip-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 16px 0;
  }

  .chip {
    background: var(--bg);
    color: var(--accent);
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    border: 1px solid var(--border);
  }

  .cta {
    margin-top: 12px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--accent);
    font-weight: 600;
  }

  .book-preview {
    background: var(--surface);
    border-radius: 16px;
    padding: 16px;
    border: 1px solid var(--border);

    ul {
      margin-top: 12px;
      display: grid;
      gap: 4px;
      font-size: 0.95rem;
    }
  }
}
</style>

