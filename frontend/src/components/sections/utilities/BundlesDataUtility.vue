<template>
  <div class="utility-card">
    <h3 class="utility-title">Bundles Procesados</h3>
    <p class="utility-description">
      Explora y visualiza los bundles procesados y almacenados en la base de datos.
    </p>

    <div v-show="error" class="error-message">
      {{ error }}
    </div>

    <div v-show="loading" class="loading">
      Cargando bundles...
    </div>

    <div v-if="!loading && !error" class="bundles-container">
      <!-- Estadísticas -->
      <div class="stats-section">
        <div class="stat-card">
          <div class="stat-value">{{ bundles.length }}</div>
          <div class="stat-label">Total Bundles</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ activeBundles.length }}</div>
          <div class="stat-label">Activos</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ inactiveBundles.length }}</div>
          <div class="stat-label">Inactivos</div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters-section">
        <div class="filter-group">
          <label class="filter-label">Estado:</label>
          <select v-model="statusFilter" class="filter-select">
            <option value="all">Todos</option>
            <option value="active">Activos</option>
            <option value="inactive">Inactivos</option>
          </select>
        </div>
        <button @click="loadData" class="refresh-button" :disabled="loading">
          {{ loading ? "Cargando..." : "Actualizar" }}
        </button>
      </div>

      <!-- Lista de bundles -->
      <div class="bundles-list">
        <div v-if="filteredBundles.length === 0" class="empty-state">
          No hay bundles que coincidan con los filtros seleccionados.
        </div>
        
        <div
          v-for="bundle in filteredBundles"
          :key="bundle.id"
          class="bundle-item"
          :class="{ active: bundle.is_active, inactive: !bundle.is_active }"
        >
          <div class="bundle-header" @click="toggleBundle(bundle.id)">
            <div class="bundle-info">
              <h4 class="bundle-name">
                {{ bundle.tile_short_name || bundle.tile_name || bundle.machine_name }}
              </h4>
              <div class="bundle-meta">
                <span v-if="bundle.is_active" class="bundle-status active">
                  ✓ Activo
                </span>
                <span v-else class="bundle-status inactive">
                  ⊗ Inactivo
                </span>
                <span v-if="bundle.verification_date" class="bundle-date">
                  📅 {{ formatDate(bundle.verification_date) }}
                </span>
              </div>
            </div>
            <button class="expand-btn" :aria-expanded="expandedBundles === bundle.id">
              <span class="expand-icon">{{ expandedBundles === bundle.id ? '−' : '+' }}</span>
            </button>
          </div>

          <div v-show="expandedBundles === bundle.id" class="bundle-details">
            <div class="details-grid">
              <div class="detail-item">
                <strong>ID:</strong> {{ bundle.id }}
              </div>
              <div class="detail-item">
                <strong>Machine Name:</strong> {{ bundle.machine_name }}
              </div>
              <div v-if="bundle.product_url" class="detail-item">
                <strong>URL:</strong>
                <a :href="bundle.product_url" target="_blank" rel="noopener">
                  {{ bundle.product_url }}
                </a>
              </div>
              <div v-if="bundle.start_date_datetime" class="detail-item">
                <strong>Inicio:</strong> {{ formatDate(bundle.start_date_datetime) }}
              </div>
              <div v-if="bundle.end_date_datetime" class="detail-item">
                <strong>Fin:</strong> {{ formatDate(bundle.end_date_datetime) }}
              </div>
              <div v-if="bundle.duration_days" class="detail-item">
                <strong>Duración:</strong> {{ bundle.duration_days }} días
              </div>
              <div v-if="bundle.msrp_total" class="detail-item">
                <strong>MSRP Total:</strong> ${{ bundle.msrp_total.toFixed(2) }}
              </div>
              <div v-if="bundle.price_tiers && bundle.price_tiers.length > 0" class="detail-item full-width">
                <strong>Precios:</strong>
                <div class="price-tiers">
                  <div
                    v-for="(tier, idx) in bundle.price_tiers"
                    :key="idx"
                    class="price-tier"
                  >
                    <span class="tier-name">{{ tier.header || tier.identifier }}</span>
                    <span v-if="tier.price" class="tier-price">
                      {{ tier.price.currency }} {{ tier.price.amount }}
                    </span>
                  </div>
                </div>
              </div>
              <div v-if="bundle.book_list && bundle.book_list.length > 0" class="detail-item full-width">
                <strong>Libros ({{ bundle.book_list.length }}):</strong>
                <div 
                  class="books-preview"
                  :class="{ expanded: expandedBooks.has(bundle.id) }"
                  @click.stop="toggleBooks(bundle.id)"
                >
                  <div
                    v-for="(book, idx) in (expandedBooks.has(bundle.id) ? bundle.book_list : bundle.book_list.slice(0, 5))"
                    :key="book.machine_name || idx"
                    class="book-preview-item"
                  >
                    {{ book.title || book.machine_name }}
                  </div>
                  <div 
                    v-if="bundle.book_list.length > 5 && !expandedBooks.has(bundle.id)" 
                    class="more-books clickable"
                  >
                    +{{ bundle.book_list.length - 5 }} más (click para expandir)
                  </div>
                  <div 
                    v-if="expandedBooks.has(bundle.id) && bundle.book_list.length > 5" 
                    class="more-books clickable"
                  >
                    (click para colapsar)
                  </div>
                </div>
              </div>
            </div>
            <div class="bundle-actions">
              <button
                @click.stop="viewBundleJson(bundle)"
                class="action-btn view-btn"
              >
                🔍 Ver JSON
              </button>
              <button
                @click.stop="downloadBundleJson(bundle)"
                class="action-btn download-btn"
              >
                ⬇ Descargar JSON
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useBundles } from "@/composables/useBundles";
import type { Bundle } from "@/types/bundle";

const { bundles, loading, error, refresh } = useBundles();

const statusFilter = ref<"all" | "active" | "inactive">("all");
const expandedBundles = ref<string | null>(null);
const expandedBooks = ref<Set<string>>(new Set());

const activeBundles = computed(() =>
  bundles.value.filter((b) => b.is_active)
);

const inactiveBundles = computed(() =>
  bundles.value.filter((b) => !b.is_active)
);

const filteredBundles = computed(() => {
  let filtered = bundles.value;

  // Filtrar por estado
  if (statusFilter.value === "active") {
    filtered = filtered.filter((b) => b.is_active);
  } else if (statusFilter.value === "inactive") {
    filtered = filtered.filter((b) => !b.is_active);
  }

  // Ordenar: activos primero, luego por fecha de verificación
  return filtered.sort((a, b) => {
    if (a.is_active !== b.is_active) {
      return a.is_active ? -1 : 1;
    }
    const dateA = a.verification_date ? new Date(a.verification_date).getTime() : 0;
    const dateB = b.verification_date ? new Date(b.verification_date).getTime() : 0;
    return dateB - dateA; // Más recientes primero
  });
});

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString("es-ES", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function toggleBundle(bundleId: string) {
  if (expandedBundles.value === bundleId) {
    expandedBundles.value = null;
    expandedBooks.value.delete(bundleId);
  } else {
    expandedBundles.value = bundleId;
    expandedBooks.value.delete(bundleId);
  }
}

function toggleBooks(bundleId: string) {
  if (expandedBooks.value.has(bundleId)) {
    expandedBooks.value.delete(bundleId);
  } else {
    expandedBooks.value.add(bundleId);
  }
}

function viewBundleJson(bundle: Bundle) {
  const jsonString = JSON.stringify(bundle, null, 2);
  const blob = new Blob([jsonString], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  window.open(url, "_blank");
  URL.revokeObjectURL(url);
}

function downloadBundleJson(bundle: Bundle) {
  const jsonString = JSON.stringify(bundle, null, 2);
  const blob = new Blob([jsonString], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `bundle-${bundle.machine_name || bundle.id}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function loadData() {
  refresh();
}

onMounted(() => {
  loadData();
});
</script>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.utility-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;

  .utility-title {
    font-size: 1.5rem;
    color: var(--accent);
    margin: 0 0 12px 0;
  }

  .utility-description {
    color: var(--text);
    margin: 0 0 24px 0;
    opacity: 0.9;
  }
}

.error-message {
  background: var(--error-bg);
  border: 1px solid var(--error-border);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: var(--error-red);
}

.loading {
  text-align: center;
  padding: 24px;
  color: var(--text);
  opacity: 0.7;
}

.bundles-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 16px;

  .stat-card {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    text-align: center;

    .stat-value {
      font-size: 2rem;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 0.9rem;
      color: var(--text);
      opacity: 0.8;
    }
  }
}

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

  .refresh-button {
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: opacity 0.2s;
    height: fit-content;

    &:hover:not(:disabled) {
      opacity: 0.9;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}

.bundles-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 800px;
  overflow-y: auto;
  padding: 8px;
}

.empty-state {
  padding: 48px;
  text-align: center;
  color: var(--text);
  opacity: 0.7;
  font-size: 1.1rem;
}

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

  .bundle-details {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border);

    .details-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
      margin-bottom: 16px;

      .detail-item {
        font-size: 0.9rem;
        color: var(--text);

        strong {
          color: var(--accent);
          margin-right: 8px;
        }

        a {
          color: var(--button-blue);
          text-decoration: none;

          &:hover {
            text-decoration: underline;
          }
        }

        &.full-width {
          grid-column: 1 / -1;
        }
      }

      .price-tiers {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 8px;

        .price-tier {
          display: flex;
          justify-content: space-between;
          padding: 8px;
          background: var(--background);
          border-radius: 6px;
          border: 1px solid var(--border);

          .tier-name {
            font-weight: 600;
          }

          .tier-price {
            color: var(--accent);
            font-weight: 600;
          }
        }
      }

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
    }

    .bundle-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      padding-top: 16px;
      border-top: 1px dashed var(--border);

      .action-btn {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;

        &:hover {
          opacity: 0.9;
          transform: translateY(-1px);
        }

        &.view-btn {
          background: var(--button-blue);
        }

        &.download-btn {
          background: var(--button-green);
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .utility-card {
    padding: 16px;
  }

  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .filters-section {
    flex-direction: column;
    align-items: stretch;

    .filter-group {
      width: 100%;

      .filter-select {
        width: 100%;
      }
    }

    .refresh-button {
      width: 100%;
    }
  }

  .bundle-item {
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

