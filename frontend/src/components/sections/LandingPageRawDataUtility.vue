<template>
  <div class="utility-card">
    <h3 class="utility-title">{{ $t('rawDataUtility.title') }}</h3>
    <p class="utility-description">
      {{ $t('rawDataUtility.description') }}
    </p>

    <div v-show="error" class="error-message">
      {{ error }}
    </div>

    <div v-show="isListLoading" class="loading">
      {{ $t('rawDataUtility.loading') }}
    </div>

    <div class="raw-data-container">
      <div class="records-section">
        <h4>{{ $t('rawDataUtility.storedRecords') }}</h4>
        <button @click="loadData" class="refresh-button" :disabled="isListLoading">
          {{ isListLoading ? $t('rawDataUtility.loading') : $t('rawDataUtility.updateList') }}
        </button>
        
        <div v-if="rawDataList.length === 0" class="empty-state">
          {{ $t('rawDataUtility.emptyState') }}
        </div>
        
        <div v-else class="records-list">
          <div
            v-for="record in rawDataList"
            :key="record.id"
            class="record-item"
          >
            <div class="record-content">
              <div class="record-header">
                <div class="record-date-section">
                  <span class="record-label">{{ $t('rawDataUtility.date') }}</span>
                  <span class="record-date">{{ formatDate(record.scraped_date) }}</span>
                </div>
                <div v-if="record.json_hash" class="record-hash-section">
                  <span class="record-label">{{ $t('rawDataUtility.hash') }}</span>
                  <span class="record-hash" :title="record.json_hash">
                    {{ record.json_hash.substring(0, 12) }}...
                  </span>
                </div>
              </div>
              <div class="record-meta">
                <span class="record-label">{{ $t('rawDataUtility.url') }}</span>
                <span class="record-source">{{ record.source_url }}</span>
              </div>
              <div v-if="record.json_version" class="record-version">
                <span class="record-label">{{ $t('rawDataUtility.version') }}</span>
                <span>{{ record.json_version }}</span>
              </div>
              <div class="record-actions">
                <button 
                  @click.stop="openJsonInNewTab(record)" 
                  class="record-action-btn open-btn"
                  :title="$t('rawDataUtility.openJsonTitle')"
                >
                  {{ $t('rawDataUtility.openJson') }}
                </button>
                <button 
                  @click.stop="downloadRecordJson(record)" 
                  class="record-action-btn download-btn"
                  :title="$t('rawDataUtility.downloadTitle')"
                >
                  {{ $t('rawDataUtility.download') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="selectedRecord || isDetailLoading" class="json-section">
        <div class="json-header">
          <h4>{{ $t('rawDataUtility.jsonData') }}</h4>
          <div class="json-actions">
            <button @click="copyJson" class="action-button" :disabled="isDetailLoading || !selectedRecord">{{ $t('rawDataUtility.copyJson') }}</button>
            <button @click="downloadJson" class="action-button" :disabled="isDetailLoading || !selectedRecord">{{ $t('rawDataUtility.downloadJson') }}</button>
            <span v-show="copySuccess" class="copy-feedback">{{ $t('rawDataUtility.copied') }}</span>
          </div>
        </div>
        <div v-show="isDetailLoading" class="detail-loading">{{ $t('rawDataUtility.loadingDetail') }}</div>
        <div v-if="selectedRecord">
          <div class="json-meta">
            <div class="meta-item">
              <strong>{{ $t('rawDataUtility.date') }}</strong> {{ formatDate(selectedRecord.scraped_date) }}
            </div>
            <div class="meta-item">
              <strong>{{ $t('rawDataUtility.url') }}</strong> {{ selectedRecord.source_url }}
            </div>
            <div v-if="selectedRecord.json_hash" class="meta-item">
              <strong>{{ $t('rawDataUtility.hash') }}</strong> {{ selectedRecord.json_hash }}
            </div>
            <div class="meta-item">
              <strong>{{ $t('rawDataUtility.size') }}</strong> {{ formatJsonSize(formattedJson) }}
            </div>
          </div>
          <div class="json-viewer">
            <pre class="json-content"><code>{{ formattedJson }}</code></pre>
          </div>
        </div>
        <div v-else class="detail-loading">{{ $t('rawDataUtility.selectRecord') }}</div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRawData } from "@/composables/useRawData";
import type { LandingPageRawData } from "@/types/rawData";

const { locale } = useI18n();

const {
  rawDataList,
  error,
  fetchRawDataList,
} = useRawData();

const selectedRecord = ref<LandingPageRawData | null>(null);
const copySuccess = ref(false);
const isListLoading = ref(false);
const isDetailLoading = ref(false);

const formattedJson = computed(() => {
  if (!selectedRecord.value) return "";
  return JSON.stringify(selectedRecord.value.json_data, null, 2);
});

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const dateLocale = locale.value === 'es' ? 'es-ES' : 'en-US';
  return date.toLocaleString(dateLocale, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

async function loadData() {
  isListLoading.value = true;
  await fetchRawDataList();
  isListLoading.value = false;

  if (error.value || rawDataList.value.length === 0) {
    selectedRecord.value = null;
    return;
  }

  // Ya no se selecciona automáticamente el primer registro
}


async function copyJson() {
  if (!formattedJson.value) return;
  
  try {
    await navigator.clipboard.writeText(formattedJson.value);
    copySuccess.value = true;
    setTimeout(() => {
      copySuccess.value = false;
    }, 2000);
  } catch (err) {
    console.error("Error al copiar:", err);
  }
}

function downloadJson() {
  if (!formattedJson.value || !selectedRecord.value) return;
  
  const blob = new Blob([formattedJson.value], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `landing-page-raw-data-${selectedRecord.value.id}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function formatJsonSize(json: string): string {
  const bytes = new Blob([json]).size;
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function openJsonInNewTab(record: LandingPageRawData) {
  const jsonString = JSON.stringify(record.json_data, null, 2);
  const blob = new Blob([jsonString], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  window.open(url, "_blank");
  // Limpiar el URL después de un tiempo para liberar memoria
  setTimeout(() => URL.revokeObjectURL(url), 100);
}

function downloadRecordJson(record: LandingPageRawData) {
  const jsonString = JSON.stringify(record.json_data, null, 2);
  const blob = new Blob([jsonString], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `landing-page-raw-data-${record.id}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}


onMounted(() => {
  loadData();
});
</script>

<style scoped lang="scss">
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

.raw-data-container {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.records-section {
  h4 {
    font-size: 1.1rem;
    color: var(--accent);
    margin: 0 0 16px 0;
  }

  .refresh-button {
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    cursor: pointer;
    margin-bottom: 16px;
    font-size: 0.9rem;
    transition: opacity 0.2s;

    &:hover:not(:disabled) {
      opacity: 0.9;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }

  .empty-state {
    padding: 24px;
    text-align: center;
    color: var(--text);
    opacity: 0.7;
  }

  .records-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-height: 600px;
    overflow-y: auto;
    padding: 4px;
  }

  .record-item {
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--surface);
    transition: all 0.2s ease;
    overflow: hidden;

    &:hover {
      border-color: var(--accent);
      box-shadow: 0 2px 8px var(--shadow-black-light);
    }

    .record-content {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .record-header {
      display: flex;
      flex-direction: column;
      gap: 8px;

      .record-date-section,
      .record-hash-section {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .record-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--accent);
        min-width: 60px;
      }

      .record-date {
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--text);
      }

      .record-hash {
        font-family: monospace;
        font-size: 0.85rem;
        color: var(--text);
        opacity: 0.9;
        word-break: break-all;
      }
    }

    .record-meta {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      font-size: 0.9rem;

      .record-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--accent);
        min-width: 60px;
        flex-shrink: 0;
      }

      .record-source {
        word-break: break-all;
        color: var(--text);
        opacity: 0.9;
        flex: 1;
      }
    }

    .record-version {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
      color: var(--text);
      opacity: 0.8;

      .record-label {
        font-weight: 600;
        color: var(--accent);
        min-width: 60px;
      }
    }

    .record-actions {
      display: flex;
      gap: 8px;
      margin-top: 4px;
      padding-top: 12px;
      border-top: 1px solid var(--border);

      .record-action-btn {
        flex: 1;
        padding: 8px 12px;
        border: 1px solid var(--border);
        border-radius: 6px;
        background: var(--background);
        color: var(--text);
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;

        &:hover {
          background: var(--accent);
          color: white;
          border-color: var(--accent);
          transform: translateY(-1px);
        }

        &.open-btn {
          &:hover {
            background: var(--button-blue);
            border-color: var(--button-blue);
          }
        }

        &.download-btn {
          &:hover {
            background: var(--button-green);
            border-color: var(--button-green);
          }
        }
      }
    }
  }
}

.json-section {
  h4 {
    font-size: 1.1rem;
    color: var(--accent);
    margin: 0 0 16px 0;
  }

  .json-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    @media (max-width: 768px) {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
    }
  }

  .json-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;

    .action-button {
      background: var(--accent);
      color: white;
      border: none;
      border-radius: 8px;
      padding: 8px 16px;
      cursor: pointer;
      font-size: 0.9rem;
      transition: opacity 0.2s;

      &:hover {
        opacity: 0.9;
      }

      &.primary {
        background: var(--accent);
        font-weight: 600;
      }
    }

    .copy-feedback {
      color: var(--accent);
      font-weight: 600;
      align-self: center;
    }
  }

  .json-meta {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 16px;
    font-size: 0.9rem;

    .meta-item {
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }

      strong {
        color: var(--accent);
        margin-right: 8px;
      }
    }
  }

  .json-viewer {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-top: 16px;
    overflow: auto;
    max-height: 600px;

    .json-content {
      margin: 0;
      padding: 20px;
      font-family: "Monaco", "Menlo", "Ubuntu Mono", "Consolas", "source-code-pro", monospace;
      font-size: 13px;
      line-height: 1.6;
      color: var(--text);
      white-space: pre;
      overflow-x: auto;

      code {
        color: var(--text);
        font-family: inherit;
      }
    }
  }
}

.detail-loading {
  margin-bottom: 8px;
  color: var(--text);
  opacity: 0.8;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .utility-card {
    padding: 16px;
  }

  .raw-data-container {
    gap: 16px;
  }
}
</style>
