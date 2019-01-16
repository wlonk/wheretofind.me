<template>
  <div class="card">
    <div class="card-body">
      <div class="form-group row">
        <label :for="nameLabel" class="col-sm-2 col-form-label">Name</label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="name"
            v-model="identity.name"
            @blur="updateIdentity"
            :id="nameLabel"
            :disabled="disabled"
          />
        </div>
      </div>
      <div class="form-group row">
        <label :for="urlLabel" class="col-sm-2 col-form-label">URL</label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="url"
            v-model="identity.url"
            @blur="updateIdentity"
            :id="urlLabel"
            :disabled="disabled"
          />
        </div>
      </div>
      <div class="d-none float-left msg-saving">Saving…</div>
      <div class="d-none float-left msg-deleting">Deleting…</div>
      <button
        class="btn delete btn-outline-danger float-right"
        @click="deleteIdentity"
      >
        <span class="fas fa-minus-circle"></span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Identity",
  props: ["identity", "disabled"],
  computed: {
    nameLabel() {
      return `name-${this.identity.id}`;
    },
    urlLabel() {
      return `url-${this.identity.id}`;
    }
  },
  methods: {
    updateIdentity() {
      // TODO flash "saving" div.
      this.$emit("updateIdentity", this.identity);
    },
    deleteIdentity() {
      // TODO flash "deleting" div.
      this.$emit("deleteIdentity", this.identity);
    }
  }
};
</script>

<style></style>
