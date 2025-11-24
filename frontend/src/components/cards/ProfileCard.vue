<template>
  <section class="profile">
    <div class="profile-image">
      <img 
        :src="profileImage" 
        :alt="$t('profile.name')"
        @error="handleImageError"
      />
    </div>
    <div class="profile-name">
      <h2>{{ $t('profile.name') }}</h2>
      <p>{{ $t('profile.tagline') }}</p>
    </div>
    <div class="profile-description">
      <p>{{ $t('profile.description') }}</p>
    </div>
    <div class="profile-links">
      <a 
        v-for="link in profileLinks" 
        :key="link.name"
        :href="link.url" 
        target="_blank"
        rel="noopener noreferrer"
        class="profile-link"
      >
        <span class="link-icon">{{ link.icon }}</span>
        <span>{{ link.name }}</span>
      </a>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// Imágenes de perfil de dynamic-portafolio-hub
const profileImages = [
  'https://avatars.githubusercontent.com/u/dopeldev',
  'https://github.com/dopeldev.png',
  'https://dopeldev.github.io/dynamic-portafolio-hub/profile.jpg',
  'https://dopeldev.github.io/dynamic-portafolio-hub/profile.png',
  '/profile.jpg',
  '/profile.png'
];

const profileImage = ref(profileImages[0]);
const imageErrorCount = ref(0);

const handleImageError = () => {
  imageErrorCount.value++;
  if (imageErrorCount.value < profileImages.length) {
    profileImage.value = profileImages[imageErrorCount.value];
  } else {
    // Fallback a placeholder SVG
    profileImage.value = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTEwIiBoZWlnaHQ9IjExMCIgdmlld0JveD0iMCAwIDExMCAxMTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iNTUiIGN5PSI1NSIgcj0iNTUiIGZpbGw9InZhcigtLXN1cmZhY2UpIi8+PHRleHQgeD0iNTUiIHk9IjY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iNDAiIGZpbGw9InZhcigtLW11dGVkKSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RDwvdGV4dD48L3N2Zz4=';
  }
};

const profileLinks = [
  {
    name: 'GitHub',
    url: 'https://github.com/dopeldev',
    icon: '↗'
  },
  {
    name: 'LinkedIn',
    url: 'https://www.linkedin.com/in/pedro-gonzales-32505758',
    icon: '↗'
  },
  {
    name: 'Portfolio',
    url: 'https://www.dopeldev.com/',
    icon: '↗'
  }
];
</script>

<style scoped lang="scss">
.profile {
  background: var(--border);
  padding: 24px;
  border-radius: 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 16px;

  .profile-image {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: var(--surface);
    margin: 0 auto;
    overflow: hidden;
    border: 3px solid var(--accent);
    box-shadow: 0 4px 12px var(--shadow-black);

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .profile-name {
    color: var(--accent);
    margin: 0;

    h2 {
      margin: 0 0 4px 0;
      font-size: 1.5rem;
    }

    p {
      margin: 0;
      font-size: 0.9rem;
      color: var(--muted);
      font-weight: 500;
    }
  }

  .profile-description {
    color: var(--text);
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
  }

  .profile-links {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 8px;

    .profile-link {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 16px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 500;
      transition: all 0.2s ease;

      .link-icon {
        font-size: 0.85rem;
        opacity: 0.7;
      }

      &:hover {
        background: var(--accent);
        color: white;
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow-black);

        .link-icon {
          opacity: 1;
        }
      }

      &:active {
        transform: translateY(0);
      }
    }
  }
}
</style>

