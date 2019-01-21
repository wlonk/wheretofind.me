<template>
  <button
    type="button"
    class="btn add-alias btn-outline-primary float-right"
    @click.prevent="createAlias"
  >
    <span class="fas fa-plus-circle"></span>
  </button>
</template>

<script>
export default {
  name: 'AddAliasButton',
  methods: {
    createAlias() {
      this.$emit('createAlias');
    },
  },
};
</script>
