<template>
  <div class="alias card bg-light shadow-sm w-100 mb-3">
    <div class="card-body drag-indicator">
      <div class="form-group row">
        <label :for="nameLabel" class="col-sm-2 col-form-label">Name</label>
        <div class="col-sm-9">
          <input
            type="text"
            class="form-control"
            name="name"
            v-model="alias.name"
            @blur="update"
            @keyup.enter="update"
            :id="nameLabel"
            :disabled="disabled"
          />
        </div>
        <div class="col-sm-1" v-if="index > 0">
          <button
            type="button"
            class="btn btn-outline-danger float-right"
            @click="destroy"
          >
            <span class="fas fa-minus-circle"></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Alias',
  props: ['alias', 'disabled', 'index'],
  computed: {
    nameLabel() {
      return `name-${this.alias.id}`;
    },
  },
  methods: {
    update() {
      const url = window.Urls['api:alias-detail'](this.alias.id);
      const data = this.alias;
      return this.$http.put(url, data);
    },
    destroy() {
      // TODO flash "deleting" div.
      this.$emit('destroy', this.alias);
    },
  },
};
</script>

<style scoped>
.drag-indicator {
  cursor: grab;
}
.alias {
  background: url('../images/draghandle.png') no-repeat bottom 2px left 3px;
}
</style>
