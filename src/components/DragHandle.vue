<template>
  <div
    @keydown.prevent.stop.up.down="rearrangeSelf"
    :tabIndex="tabIndex"
    class="card-control-icon rearrange-handle"
  ></div>
</template>

<script>
export default {
  props: ['itemIndex', 'tabIndex'],
  methods: {
    rearrangeSelf(e) {
      const eventObject = {
        index: this.itemIndex,
        // Needed so that the form can keep the handle in focus after
        // rearranging things:
        handle: this.$el,
        // Needed so that the form can monitor whether this identity's html
        // element is still in view or not:
        el: this.$parent.$el,
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
      this.$parent.$emit('moved', eventObject);
    },
  },
};
</script>

<style scoped>
.card-control-icon {
  bottom: 0;
  cursor: grab;
  height: 30px;
  position: absolute;
  right: 0;
  width: 30px;
}
</style>
