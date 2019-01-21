<template>
  <div class="identity card bg-light shadow-sm w-100 mb-3">
    <div class="card-body drag-indicator">
      <div class="form-group row">
        <label :for="nameLabel" class="col-sm-2 col-form-label">Name</label>
        <div class="col-sm-9">
          <input
            type="text"
            class="form-control"
            name="name"
            :tabindex="nameTabIndex"
            v-model="identity.name"
            @blur="updateIdentity"
            @keyup.enter="updateIdentity"
            :id="nameLabel"
            :disabled="disabled"
          />
        </div>
        <div class="col-sm-1">
          <button
            type="button"
            class="btn delete btn-outline-danger float-right"
            :tabindex="deleteTabIndex"
            @click="deleteIdentity"
          >
            <span class="fas fa-minus-circle"></span>
          </button>
        </div>
      </div>
      <div class="form-group row">
        <label :for="urlLabel" class="col-sm-2 col-form-label">URL</label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="url"
            :tabindex="urlTabIndex"
            v-model="identity.url"
            @blur="updateIdentity"
            @keyup.enter="updateIdentity"
            :id="urlLabel"
            :disabled="disabled"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Identity',
  props: ['identity', 'disabled', 'index'],
  computed: {
    nameLabel() {
      return `name-${this.identity.id}`;
    },
    urlLabel() {
      return `url-${this.identity.id}`;
    },
    nameTabIndex() {
      return this.index * 10 + 1;
    },
    urlTabIndex() {
      return this.index * 10 + 2;
    },
    deleteTabIndex() {
      return this.index * 10 + 3;
    },
  },
  methods: {
    updateIdentity() {
      const url = window.Urls['api:identity-detail'](this.identity.id);
      const data = this.identity;
      return this.$http.put(url, data);
    },
    deleteIdentity() {
      // TODO flash "deleting" div.
      this.$emit('deleteIdentity', this.identity);
    },
  },
};
</script>

<style scoped>
.drag-indicator {
  cursor: grab;
}
.identity {
  background: url('../images/draghandle.png') no-repeat bottom 2px left 3px;
}
</style>
