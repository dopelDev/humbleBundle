<template>
  <article class="bundle-card" :id="`bundle-${bundle.id}`" @click="openModal">
    <h3>{{ bundle.tile_short_name ?? bundle.tile_name }}</h3>
    <p class="meta">
      {{ bundle.category }} • Termina {{
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
      Ver bundle →
    </a>
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
import type { Bundle } from "@/types/bundle";
import BookModal from "./BookModal.vue";

defineProps<{ bundle: Bundle }>();

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const formatDate = (value?: string) => {
  if (!value) return "—";
  return new Date(value).toLocaleDateString("es-PE", {
    month: "short",
    day: "numeric"
  });
};
</script>

<style scoped lang="scss">
.bundle-card {
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;

  &:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  h3 {
    font-size: 1.1rem;
    color: var(--accent);
  }

  .meta {
    font-size: 0.85rem;
    color: var(--text);
  }

  .msrp {
    font-weight: 600;
    color: var(--primary);
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

