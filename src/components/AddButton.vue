<template>
  <button
    type="button"
    tabindex="1000"
    class="btn add-identity btn-outline-primary float-right"
    @click.prevent="create"
  >
    <span class="fas fa-plus-circle"></span>
  </button>
</template>

<script>
export default {
  name: 'AddButton',
  methods: {
    create() {
      this.$emit('create');
    },
  },
};
</script>
