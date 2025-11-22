<template>
  <section class="profile">
    <div class="profile-image"></div>
    <div class="profile-name">
      <h2>{{ $t('profile.name') }}</h2>
      <p>{{ $t('profile.tagline') }}</p>
    </div>
    <div class="profile-description">
      <p>
        {{ $t('profile.description') }}
      </p>
    </div>
  </section>
</template>

<style scoped lang="scss">
.profile {
  background: var(--border);
  padding: 24px;
  border-radius: 24px;
  text-align: center;

  .profile-image {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: var(--surface);
    margin: 0 auto 16px;
  }

  .profile-name {
    color: var(--accent);
    margin-bottom: 12px;
  }

  .profile-description {
    color: var(--text);
    font-size: 0.95rem;
  }
}
</style>

