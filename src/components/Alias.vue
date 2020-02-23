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
    <div
      @keydown.prevent.stop.up.down="rearrangeSelf"
      :tabIndex="moveTabIndex"
      class="card-control-icon rearrange-handle"
      ref="rearrangeHandle"
    ></div>
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
    rearrangeSelf(e) {
      const eventObject = {
        index: this.index,
        // Needed so that the form can keep the handle in focus after
        // rearranging things:
        handle: this.$refs.rearrangeHandle,
        // Needed so that the form can monitor whether this identity's html
        // element is still in view or not:
        el: this.$el,
      };
      switch (e.keyCode) {
        case 38:
          eventObject.direction = 'up';
          break;
        case 40:
          eventObject.direction = 'down';
          break;
        // No default is necessary, as the Vue template bindings prevent any
        // other possible values.
      }
      this.$emit('moved', eventObject);
    },
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
  background: url('../images/draghandle-right.png') no-repeat bottom 2px right
    3px;
}
.card-control-icon {
  bottom: 0;
  cursor: grab;
  height: 30px;
  position: absolute;
  right: 0;
  width: 30px;
}
</style>
