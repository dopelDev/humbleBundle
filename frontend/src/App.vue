<template>
  <div class="app-shell" :class="`locale-${locale}`">
    <DarkButton />
    <LanguageSwitcher />
    
    <section class="intro">
      <ProfileCard />
      <div class="status-card">
        <p class="eyebrow">{{ $t('app.eyebrow') }}</p>
        <h1>{{ $t('app.title') }}</h1>
        <p class="project-description">{{ $t('app.description') }}</p>
        
        <div class="project-info">
          <div class="tech-stack">
            <h3>{{ $t('app.techStack.title') }}</h3>
            <ul>
              <li>{{ $t('app.techStack.backend') }}</li>
              <li>{{ $t('app.techStack.frontend') }}</li>
              <li>{{ $t('app.techStack.scraping') }}</li>
            </ul>
          </div>
          
          <div class="endpoints">
            <h3>{{ $t('app.endpoints.title') }}</h3>
            <ul>
              <li><code>{{ $t('app.endpoints.health') }}</code></li>
              <li><code>{{ $t('app.endpoints.bundles') }}</code></li>
              <li><code>{{ $t('app.endpoints.bundleById') }}</code></li>
              <li><code>{{ $t('app.endpoints.bundleByName') }}</code></li>
              <li><code>{{ $t('app.endpoints.featured') }}</code></li>
              <li><code>{{ $t('app.endpoints.etl') }}</code></li>
              <li><code>{{ $t('app.endpoints.rawData') }}</code></li>
            </ul>
          </div>
        </div>
        
        <div class="stats" v-show="!loading">
          <span><strong>{{ bundles.length }}</strong> {{ $t('app.stats.totalBundles') }}</span>
          <span><strong>{{ activeBundles.length }}</strong> {{ $t('app.stats.active') }}</span>
        </div>
        <div class="last-update" v-show="lastUpdate">
          <span>{{ $t('app.lastUpdate') }} {{ lastUpdate ? formatDate(lastUpdate) : '' }}</span>
        </div>
        <button class="refresh" @click="runETL" :disabled="loading">
          {{ loading ? $t('app.buttons.updating') : $t('app.buttons.updateData') }}
        </button>
        <p v-show="error" class="error">{{ error }}</p>
        
        <div v-if="etlResult" class="etl-result">
          <h4>{{ $t('app.etlResult.title') }}</h4>
          <ul>
            <li><strong>{{ etlResult.bundles_processed }}</strong> {{ $t('app.etlResult.bundlesProcessed') }}</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="tabs-container">
      <div class="tabs-nav">
        <button
          class="tab-button"
          :class="{ active: activeTab === 'bundles' }"
          @click="activeTab = 'bundles'"
        >
          {{ $t('app.tabs.activeBundles') }}
        </button>
        <button
          class="tab-button"
          :class="{ active: activeTab === 'tests' }"
          @click="activeTab = 'tests'"
        >
          {{ $t('app.tabs.testsAndUtilities') }}
        </button>
      </div>

      <div v-show="activeTab === 'bundles'" class="tab-content">
        <component
          :is="isMobile ? MobileMain : DesktopMain"
          :bundles="activeBundles"
          :featured="featured"
        />
      </div>

      <div v-show="activeTab === 'tests'" class="tab-content">
        <TestsSection />
        <UtilitiesSection />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import DarkButton from "@components/header/components/DarkButton.vue";
import LanguageSwitcher from "@components/header/components/LanguageSwitcher.vue";
import ProfileCard from "@components/cards/ProfileCard.vue";
import DesktopMain from "@components/main/DesktopMain.vue";
import MobileMain from "@components/main/MobileMain.vue";
import TestsSection from "@components/sections/TestsSection.vue";
import UtilitiesSection from "@components/sections/UtilitiesSection.vue";

import { useResponsiveQueryEvent } from "@composables/useResponsiveQueryEvent";
import { useBundles } from "@composables/useBundles";

const { locale } = useI18n();
const { isMobile } = useResponsiveQueryEvent();
const { bundles, featured, activeBundles, loading, error, lastUpdate, etlResult, runETL } =
  useBundles();

const activeTab = ref<'bundles' | 'tests'>('bundles');

const formatDate = (date: Date) => {
  const dateLocale = locale.value === 'es' ? 'es-ES' : 'en-US';
  return new Intl.DateTimeFormat(dateLocale, {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'America/Lima'
  }).format(date);
};
</script>

<style scoped lang="scss">
.intro {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  padding: 32px;

  .status-card {
    border-radius: 24px;
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;

    .eyebrow {
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 0.75rem;
      color: var(--primary);
    }

    h1 {
      font-size: 2rem;
      color: var(--accent);
    }

    .project-description {
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--text);
      margin-bottom: 20px;
    }

    .project-info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-bottom: 20px;
      padding: 16px;
      background: var(--surface);
      border-radius: 12px;
      border: 1px solid var(--border);

      h3 {
        margin: 0 0 12px 0;
        font-size: 1rem;
        color: var(--accent);
        font-weight: 600;
      }

      ul {
        margin: 0;
        padding-left: 20px;
        list-style: disc;
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-size: 0.85rem;
        color: var(--text);

        li {
          line-height: 1.5;

          code {
            background: var(--bg);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monofur Nerd Font', monospace;
            font-size: 0.8rem;
            color: var(--primary);
            border: 1px solid var(--border);
          }
        }
      }
    }

    .stats {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      font-size: 0.95rem;
    }

    .last-update {
      font-size: 0.85rem;
      color: var(--muted);
      opacity: 0.8;
    }

    .refresh {
      align-self: flex-start;
      background: var(--primary);
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      font-weight: 600;
      border: none;
      cursor: pointer;
      transition: background 0.3s ease, transform 0.2s ease;
      box-shadow: 0 2px 4px var(--shadow-black);

      &:hover:not(:disabled) {
        background: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow-black-medium);
      }

      &:disabled {
        background: var(--muted);
        color: var(--text);
        cursor: not-allowed;
        opacity: 0.6;
        transform: none;
      }

      &:active:not(:disabled) {
        transform: translateY(0);
      }
    }

    .error {
      color: var(--error-red-light);
      font-size: 0.9rem;
    }

    .etl-result {
      margin-top: 16px;
      padding: 16px;
      background: var(--surface);
      border-radius: 12px;
      border: 1px solid var(--border);

      h4 {
        margin: 0 0 12px 0;
        color: var(--accent);
        font-size: 1rem;
      }

      ul {
        margin: 0;
        padding-left: 20px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-size: 0.9rem;
        color: var(--text);

        li {
          strong {
            color: var(--primary);
          }
        }
      }
    }
  }
}

.tabs-container {
  margin-top: 32px;
}

.tabs-nav {
  display: flex;
  gap: 8px;
  padding: 0 32px;
  max-width: 1200px;
  margin: 0 auto;
  border-bottom: 2px solid var(--border);
  
  .tab-button {
    background: transparent;
    border: none;
    padding: 16px 24px;
    font-size: 1rem;
    font-weight: 600;
    color: var(--muted);
    cursor: pointer;
    position: relative;
    transition: color 0.3s ease;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;

    &:hover {
      color: var(--text);
    }

    &.active {
      color: var(--accent);
      border-bottom-color: var(--accent);
    }
  }
}

.tab-content {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}


@media (max-width: 768px) {
  .intro {
    padding: 16px;
  }

  .tabs-nav {
    padding: 0 16px;
    
    .tab-button {
      padding: 12px 16px;
      font-size: 0.9rem;
    }
  }

}
</style>
