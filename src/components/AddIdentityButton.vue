<template>
  <button
    class="btn add-identity btn-outline-primary float-right"
    @click.prevent="createIdentity"
  >
    <span class="fas fa-plus-circle"></span>
  </button>
</template>

<script>
export default {
  name: "AddIdentityButton",
  methods: {
    createIdentity() {
      this.$emit("createIdentity");
    }
  }
};
</script>

<style></style>
