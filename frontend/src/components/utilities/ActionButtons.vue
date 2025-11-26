<template>
  <div class="action-buttons">
    <slot />
  </div>
</template>

<style scoped lang="scss">
@use "@style/colors.scss" as *;

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 16px;
  border-top: 1px dashed var(--border);
}

@media(max-width: 600px) {
	.action-buttons {
		justify-content: center;
	}
}
</style>
