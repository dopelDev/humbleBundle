<template>
  <div class="overlay" v-if="isOpen" @click="toggleMenu"></div>
  <nav :class="['menu-mobile', { open: isOpen }]">
    <button class="hamburger" v-if="!isOpen" @click="toggleMenu">☰</button>
    <ul v-if="isOpen">
      <li v-for="item in items" :key="item.name" @click="handleAction(item)">
        {{ item.name }}
      </li>
    </ul>
  </nav>
  <DarkButton />
</template>

<script setup lang="ts">
import { ref } from "vue";
import DarkButton from "./components/DarkButton.vue";
import { useHeaderItems } from "./composables/useHeaderItems";

const isOpen = ref(false);
const { items } = useHeaderItems();

const toggleMenu = () => {
  isOpen.value = !isOpen.value;
};

const handleAction = (item: { action: () => void }) => {
  item.action();
  isOpen.value = false;
};
</script>

<style scoped lang="scss">
.menu-mobile {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  background: var(--bg);
  padding: 16px;
  transform: translateY(-100%);
  transition: transform 0.25s ease;
  z-index: 12;

  &.open {
    transform: translateY(0);
  }

  .hamburger {
    font-size: 2rem;
    color: var(--accent);
  }

  ul {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 16px;

    li {
      padding: 12px;
      border-radius: 6px;
      background: var(--surface);
      color: var(--accent);
    }
  }
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  z-index: 11;
}
</style>

