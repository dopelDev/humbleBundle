<template>
  <div class="stats-section">
    <slot />
  </div>
</template>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 16px;

  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
