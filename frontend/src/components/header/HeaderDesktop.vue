<template>
  <header class="menu-desktop">
    <nav>
      <ul>
        <li v-for="item in items" :key="item.name" @click="item.action">
          {{ item.name }}
        </li>
      </ul>
    </nav>
    <DarkButton />
  </header>
</template>

<script setup lang="ts">
import DarkButton from "./components/DarkButton.vue";
import { useHeaderItems } from "./composables/useHeaderItems";

const { items } = useHeaderItems();
</script>

<style scoped lang="scss">
.menu-desktop {
  padding: 32px;
  background: var(--bg);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48px;
  position: sticky;
  top: 0;
  z-index: 10;

  ul {
    display: flex;
    gap: 32px;
  }

  li {
    font-size: 1.2rem;
    color: var(--text);
    padding: 8px 16px;
    border-radius: 6px;
    transition:
      background 0.3s,
      transform 0.25s;

    &:hover {
      background: var(--surface);
      color: var(--accent);
      transform: translateY(-4px) scale(1.05);
    }
  }
}
</style>

