<template>
  <div class="alias draggable-item card bg-light shadow-sm w-100 mb-3">
    <div class="card-body">
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
            :tabindex="nameTabIndex"
            :id="nameLabel"
            :disabled="disabled"
          />
        </div>
        <div class="col-sm-1" v-if="index > 0">
          <button
            type="button"
            class="btn btn-outline-danger float-right"
            @click="destroy"
            aria-label="Remove alias"
            :tabindex="destroyTabIndex"
          >
            <span class="fas fa-minus-circle"></span>
          </button>
        </div>
      </div>
    </div>
    <DragHandle :tabIndex="moveTabIndex" :itemIndex="index" />
  </div>
</template>

<script>
import DragHandle from '@/components/DragHandle.vue';

export default {
  name: 'Alias',
  props: ['alias', 'disabled', 'index'],
  components: { DragHandle },
  computed: {
    nameLabel() {
      return `name-${this.alias.id}`;
    },
    nameTabIndex() {
      return this.index * 10 + 1;
    },
    destroyTabIndex() {
      return this.index * 10 + 1;
    },
    moveTabIndex() {
      return this.index * 10 + 3;
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
.alias {
  background: url('../images/draghandle-right.png') no-repeat bottom 2px right
    3px;
}
</style>
