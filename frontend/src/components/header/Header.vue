<template>
  <component :is="isMobile ? HeaderMobile : HeaderDesktop" />
</template>

<script setup lang="ts">
import { useResponsiveQueryEvent } from "@composables/useResponsiveQueryEvent";
import HeaderDesktop from "./HeaderDesktop.vue";
import HeaderMobile from "./HeaderMobile.vue";

const { isMobile } = useResponsiveQueryEvent();
</script>

<style scoped lang="scss">
:global(body) {
  background-color: var(--bg);
}
</style>

