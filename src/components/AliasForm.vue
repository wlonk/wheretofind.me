<template>
  <form @submit.prevent class="clearfix">
    <div class="pb-3 custom-control custom-switch">
      <input
        type="checkbox"
        class="custom-control-input"
        id="include-in-search"
        v-model="userInSearch"
        @change="changeUserSearchStatus"
      />
      <label class="custom-control-label" for="include-in-search">
        Include me in search results
      </label>
    </div>
    <draggable
      v-model="aliases"
      :options="draggableOptions"
      @start="startDrag"
      @end="endDrag"
    >
      <transition-group :name="!draggingInProgress ? 'rearrange' : ''">
        <Alias
          v-for="(alias, index) in aliases"
          :key="alias.id"
          :alias="alias"
          :index="index"
          :disabled="alias.disabled"
          @moved="aliasMoved"
          @destroy="destroy"
        />
      </transition-group>
    </draggable>
    <AddButton @create="create" aria-label="Add alias" />
  </form>
</template>

<script>
import Alias from '@/components/Alias.vue';
import AddButton from '@/components/AddButton.vue';
import draggable from 'vuedraggable';

export default {
  name: 'AliasForm',
  components: {
    Alias,
    AddButton,
    draggable,
  },
  props: {
    draggableOptions: {
      type: Object,
      default() {
        return {
          items: '.alias',
          axis: 'y',
          containment: 'parent',
          filter: 'input',
          preventOnFilter: false,
          handle: '.rearrange-handle',
          animation: 300,
          ghostClass: 'alias-placeholder',
        };
      },
    },
  },
  data() {
    return {
      aliases: [],
      draggingInProgress: false,
      userInSearch: false,
    };
  },
  created() {
    // TODO: this approach has a flash as the original DOM elements are
    // replaced by the Vue ones.
    this.retrieveAliases().then(resp => {
      this.aliases = resp.data;
    });
    this.retrieveSearchStatus().then(resp => {
      this.userInSearch = resp.data.search_enabled;
    });
  },
  methods: {
    /* Dragging-related methods */
    startDrag() {
      this.draggingInProgress = true;
    },
    endDrag() {
      this.draggingInProgress = false;
      this.reorder();
    },
    aliasMoved(e) {
      /// e: {
      ///   direction: 'up' | 'down',
      ///   index: number,
      ///   el: Element,
      /// }
      let newIndex;
      const validUp = e.direction === 'up' && e.index > 0;
      const validDown =
        e.direction === 'down' && e.index < this.aliases.length - 1;
      if (validUp) {
        newIndex = e.index - 1;
      } else if (validDown) {
        newIndex = e.index + 1;
      } else {
        return;
      }

      const movingAlias = this.aliases[e.index];
      this.aliases.splice(e.index, 1);
      this.aliases.splice(newIndex, 0, movingAlias);

      // For the duration of the transition as aliases are moved around,
      // this code calls requestAnimationFrame and changes the window's scroll
      // position per frame to make sure the moved alias stays in view.
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

      this.reorder();
    },
    reorder() {
      return (
        this.reorderAliases()
          // TODO: revert to pre-sorted order on error.
          .catch()
      );
    },
    create() {
      const newId =
        Math.max.apply(
          Math,
          this.aliases.map(a => a.id),
        ) + 1;
      const newAlias = {
        id: newId,
        name: '',
        disabled: true,
      };
      this.aliases.push(newAlias);
      return (
        this.createNewAlias()
          .then(resp => {
            const { id } = resp.data;
            newAlias.disabled = false;
            newAlias.id = id;
          })
          // TODO: display error state.
          .catch()
      );
    },
    destroy(alias) {
      return (
        this.destroyAlias(alias)
          .then(() => {
            const index = this.aliases.map(i => i.id).indexOf(alias.id);
            this.aliases.splice(index, 1);
          })
          // TODO: display error state.
          .catch()
      );
    },
    // API calls:
    reorderAliases() {
      const url = window.Urls['api:alias-reorder']();
      const data = this.aliases.map(i => i.id);

      return this.$http.post(url, data);
    },
    createNewAlias() {
      const url = window.Urls['api:alias-list']();
      const data = {
        name: '',
      };
      return this.$http.post(url, data);
    },
    retrieveAliases() {
      const url = window.Urls['api:alias-list']();
      return this.$http.get(url);
    },
    retrieveSearchStatus() {
      const url = window.Urls['api:profile']();
      return this.$http.get(url);
    },
    changeUserSearchStatus() {
      const url = window.Urls['api:profile']();
      const data = { search_enabled: this.userInSearch };
      return this.$http.patch(url, data);
    },
    destroyAlias(alias) {
      const url = window.Urls['api:alias-detail'](alias.id);
      return this.$http.delete(url);
    },
  },
};
</script>

<style scoped>
.alias:first-child {
  box-shadow: 0 0 5px #207e5f !important;
}
.sortable-drag {
  opacity: 1;
}
.rearrange-move {
  transition: transform 0.3s;
}
</style>
