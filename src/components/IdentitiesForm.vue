<template>
  <form @submit.prevent class="clearfix">
    <DraggableList v-model="identities" @reordered="reorder">
      <template v-slot:listItems="eventHandlers">
        <Identity
          v-for="(identity, index) in identities"
          :key="identity.id"
          :identity="identity"
          :index="index"
          :disabled="identity.disabled"
          @destroy="destroy"
          @moved="eventHandlers.moved"
          @request-started="trackRequest"
        />
      </template>
    </DraggableList>
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
import DraggableList from '@/components/DraggableList.vue';

export default {
  name: 'IdentitiesForm',
  components: {
    Identity,
    AddButton,
    DraggableList,
    SaveButton,
  },
  data() {
    return {
      identities: [],
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
    /* Event handlers
     *
     * These defer the actual API interaction to the API call methods.
     */
    reorder() {
      console.log('reorder event received');
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
</style>
