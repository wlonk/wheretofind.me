<template>
  <form @submit.prevent class="clearfix">
    <draggable
      v-model="identities"
      :options="draggableOptions"
      @start="startDrag"
      @end="endDrag"
    >
      <transition-group :name="!draggingInProgress ? 'rearrange' : ''">
        <Identity
          v-for="(identity, index) in identities"
          :key="identity.id"
          :identity="identity"
          :index="index"
          :disabled="identity.disabled"
          @destroy="destroy"
          @moved="identityMoved"
          @request-started="trackRequest"
        />
      </transition-group>
    </draggable>
    <SaveButton
      v-bind:allRequestsComplete="allRequestsComplete"
      aria-label="Save current identities"
    />
    <AddButton @create="create" aria-label="Add identity" />
  </form>
</template>

<script>
import Identity from '@/components/Identity.vue';
import AddButton from '@/components/AddButton.vue';
import SaveButton from '@/components/SaveButton.vue';
import draggable from 'vuedraggable';

export default {
  name: 'IdentitiesForm',
  components: {
    Identity,
    AddButton,
    draggable,
    SaveButton,
  },
  props: {
    draggableOptions: {
      type: Object,
      default() {
        return {
          items: '.identity',
          handle: '.rearrange-handle',
          axis: 'y',
          containment: 'parent',
          filter: 'input',
          preventOnFilter: false,
          animation: 300,
          ghostClass: 'identity-placeholder',
        };
      },
    },
  },
  data() {
    return {
      identities: [],
      draggingInProgress: false,
      runningRequests: 0,
    };
  },
  computed: {
    allRequestsComplete() {
      return this.runningRequests === 0;
    },
  },
  created() {
    // TODO: this approach has a flash as the original DOM elements are //
    // replaced by the Vue ones.
    this.retrieveIdentities().then(resp => {
      this.identities = resp.data;
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
    identityMoved(e) {
      /// e: {
      ///   direction: 'up' | 'down',
      ///   index: number,
      ///   el: Element,
      /// }
      let newIndex;
      const validUp = e.direction === 'up' && e.index > 0;
      const validDown =
        e.direction === 'down' && e.index < this.identities.length - 1;
      if (validUp) {
        newIndex = e.index - 1;
      } else if (validDown) {
        newIndex = e.index + 1;
      } else {
        return;
      }

      const movingIdentity = this.identities[e.index];
      this.identities.splice(e.index, 1);
      this.identities.splice(newIndex, 0, movingIdentity);

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

      this.reorder();
    },

    /* Event handlers
     *
     * These defer the actual API interaction to the API call methods.
     */
    reorder() {
      return (
        this.reorderIdentities()
          // TODO: revert to pre-sorted order on error.
          .catch()
      );
    },
    create() {
      const newId =
        Math.max.apply(
          Math,
          this.identities.map(i => i.id),
        ) + 1;
      const newIdentity = {
        id: newId,
        name: '',
        url: '',
        quality: 2,
        icon: 'fas fa-link',
        disabled: true,
        new: true,
      };
      this.identities.push(newIdentity);
      return (
        this.createNewIdentity()
          .then(resp => {
            const { id } = resp.data;
            newIdentity.disabled = false;
            newIdentity.id = id;
          })
          // TODO: display error state.
          .catch()
      );
    },
    destroy(identity) {
      return (
        this.destroyIdentity(identity)
          .then(() => {
            const index = this.identities.map(i => i.id).indexOf(identity.id);
            this.identities.splice(index, 1);
          })
          // TODO: display error state.
          .catch()
      );
    },

    /* Wrapper helpers to track oustanding calls
     *
     */
    trackRequest(requestRequestPromise) {
      this.runningRequests += 1;
      return requestRequestPromise.then(this.requestFinished);
    },
    requestFinished(passThrough) {
      this.runningRequests -= 1;
      return passThrough;
    },

    /* API calls: */
    reorderIdentities() {
      const url = window.Urls['api:identity-reorder']();
      const data = this.identities.map(i => i.id);
      return this.trackRequest(this.$http.post(url, data));
    },
    createNewIdentity() {
      const url = window.Urls['api:identity-list']();
      const data = {
        name: '',
        url: '',
      };
      return this.trackRequest(this.$http.post(url, data));
    },
    retrieveIdentities() {
      const url = window.Urls['api:identity-list']();
      return this.$http.get(url);
    },
    destroyIdentity(identity) {
      const url = window.Urls['api:identity-detail'](identity.id);
      return this.trackRequest(this.$http.delete(url));
    },
  },
};
</script>

<style scoped>
.sortable-drag {
  opacity: 1;
}
.rearrange-move {
  transition: transform 0.3s;
}
</style>
