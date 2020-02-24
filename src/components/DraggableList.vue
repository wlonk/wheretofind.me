<template>
  <draggable
    v-model="underlyingList"
    :options="draggableOptions"
    @start="startDrag"
    @end="endDrag"
  >
    <transition-group :move-class="draggingInProgress ? '' : 'rearrange-move'">
      <slot name="listItems" :moved="itemMoved"></slot>
    </transition-group>
  </draggable>
</template>

<script>
// INSTRUCTIONS
// This component exposes the following things: The v-model attribute is
// where you pass in the underlying data representation of your items, just like
// with v-model on `draggable` components. When you render your components you
// pass them to the listItem slot. And the listItem slot exposes the `moved`
// function, which handles `moved` events with the following event object schema:
/// e: {
///   direction: 'up' | 'down',
///   index: number,
///   el: Element (the one that is moving)
///   handle: Element (the handle that must be re-focused after the move)
/// }
// The rearrangeable elements should have the 'draggable-item' class and their
// handles should have the 'rearrange-handle' class. When a reordering is
// complete, this component emits a 'reordered' event.

import draggable from 'vuedraggable';

export default {
  components: { draggable },

  // this takes the value passed to v-model, places it in the `__underlyingListProp`
  // prop, and allows it to be updated by emitting the 'reordered' event with a
  // new array.
  model: {
    prop: '__underlyingListProp',
    event: 'reordered',
  },
  props: {
    // for simplicity, access the `underlyingList` computed property instead of
    // this, because the `underlyingList` computed property can be got And set
    __underlyingListProp: Array,

    draggableOptions: {
      type: Object,
      default() {
        return {
          animation: 200,
          axis: 'y',
          ghostClass: 'item-placeholder',
          handle: '.rearrange-handle',
          items: '.draggable-item',
          scroll: true,
          scrollSensitivity: 60,
        };
      },
    },
  },
  data() {
    return {
      draggingInProgress: false,
    };
  },
  computed: {
    // Warning: treat this as an immutable array (i. e. only get it or set it,
    // don't mutate it with something like splice(), because that won't activate
    // the setter)
    underlyingList: {
      get() {
        return this.__underlyingListProp;
      },
      set(newItemList) {
        this.$emit('reordered', newItemList);
        console.log('emitted reordered event');
      },
    },
  },
  methods: {
    startDrag() {
      this.draggingInProgress = true;
    },
    endDrag() {
      this.draggingInProgress = false;
    },
    itemMoved(e) {
      /// e: {
      ///   direction: 'up' | 'down',
      ///   index: number,
      ///   el: Element,
      ///   handle: Element
      /// }
      let newIndex;
      const validUp = e.direction === 'up' && e.index > 0;
      const validDown =
        e.direction === 'down' && e.index < this.underlyingList.length - 1;
      if (validUp) {
        newIndex = e.index - 1;
      } else if (validDown) {
        newIndex = e.index + 1;
      } else {
        return;
      }

      const movingItem = this.underlyingList[e.index];
      const newList = [...this.underlyingList];
      newList.splice(e.index, 1);
      newList.splice(newIndex, 0, movingItem);
      this.underlyingList = newList;

      // For the duration of the transition as identities are moved around,
      // this code calls requestAnimationFrame and changes the window's scroll
      // position per frame to make sure the moved identity stays in view.
      let transitionEnded = false;
      // this function does all the work and is added as a transitionstart
      // event listener:
      const keepElementInView = () => {
        const belowView =
          e.el.getBoundingClientRect().bottom > window.innerHeight;
        const aboveView = e.el.getBoundingClientRect().top < 0;
        if (belowView) {
          e.el.scrollIntoView(false);
        } else if (aboveView) {
          e.el.scrollIntoView(true);
        }
        /* istanbul ignore else */
        if (!transitionEnded) {
          window.requestAnimationFrame(keepElementInView);
        }
      };

      // This function removes the event listeners once they've outlived their
      // usefulness and is added as a transitionend listener:
      const cleanUpAfterTransition = () => {
        transitionEnded = true;
        e.el.removeEventListener('transitionstart', keepElementInView);
        e.el.removeEventListener('transitionend', cleanUpAfterTransition);
      };
      // and this is where the listeners are actually added:
      e.el.addEventListener('transitionstart', keepElementInView);
      e.el.addEventListener('transitionend', cleanUpAfterTransition);

      // This makes sure that the handle that was just used to move elements
      // stays in focus:
      this.$nextTick(() => {
        e.handle.focus();
      });
    },
  },
};
</script>

<!-- 
    if this is set to "scoped" then the transition animation won't work,
    because the actual rendered items are not, in fact, in this scope
-->
<style>
.rearrange-move {
  transition: transform 0.2s;
}
</style>
