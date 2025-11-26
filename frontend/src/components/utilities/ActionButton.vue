<template>
  <BaseButton
    :variant="computedVariant"
    :size="size"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot>{{ label }}</slot>
  </BaseButton>
</template>

<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue';

interface Props {
  variant?: 'view' | 'download' | 'primary' | 'secondary' | 'accent' | 'blue' | 'green' | 'transparent';
  size?: 'small' | 'medium' | 'large';
  label?: string;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'medium',
  label: '',
  disabled: false,
});

defineEmits<{
  click: [event: MouseEvent];
}>();

const computedVariant = computed(() => {
  if (props.variant === 'view') return 'blue';
  if (props.variant === 'download') return 'green';
  return props.variant;
});
</script>

<script lang="ts">
import { computed } from 'vue';
</script>
