<template>
  <form @submit.prevent>
    <draggable
      v-model="identities"
      :options="draggableOptions"
      @end="handleReorderIdentities"
    >
      <Identity
        v-for="identity in identities"
        :key="identity.id"
        :identity="identity"
        :disabled="identity.disabled"
        @updateIdentity="handleUpdateIdentity"
        @deleteIdentity="handleDeleteIdentity"
      />
    </draggable>
    <AddIdentityButton @createIdentity="handleCreateIdentity" />
  </form>
</template>

<script>
import Identity from './components/Identity.vue';
import AddIdentityButton from './components/AddIdentityButton.vue';
import draggable from 'vuedraggable';

export default {
  name: 'EditIdentitiesForm',
  components: {
    Identity,
    AddIdentityButton,
    draggable,
  },
  props: {
    draggableOptions: {
      type: Object,
      default() {
        return {
          items: '.identity',
          axis: 'y',
          containment: 'parent',
        };
      },
    },
  },
  data() {
    return {
      identities: [],
    };
  },
  created() {
    // TODO: this approach has a flash as the original DOM elements are
    // replaced by the Vue ones.
    this.retrieveIdentities().then(resp => {
      this.identities = resp.data;
    });
  },
  methods: {
    handleReorderIdentities() {
      this.reorderIdentities()
        // TODO: revert to pre-sorted order on error.
        .catch();
    },
    handleCreateIdentity() {
      const newIdentity = {
        id: this.identities.length + 1,
        name: '',
        url: '',
        disabled: true,
      };
      this.identities.push(newIdentity);
      this.createNewIdentity()
        .then(resp => {
          const { id } = resp.data;
          newIdentity.disabled = false;
          newIdentity.id = id;
        })
        // TODO: display error state.
        .catch();
    },
    handleUpdateIdentity(identity) {
      this.updateIdentity(identity)
        // TODO: display error state.
        .catch();
    },
    handleDeleteIdentity(identity) {
      this.deleteIdentity(identity)
        .then(() => {
          const index = this.identities.map(i => i.id).indexOf(identity.id);
          this.identities.splice(index, 1);
        })
        // TODO: display error state.
        .catch();
    },
    // API calls:
    reorderIdentities() {
      const url = window.Urls['api:identity-reorder']();
      const data = this.identities.map(i => i.id);

      return this.$http.post(url, data);
    },
    createNewIdentity() {
      const url = window.Urls['api:identity-list']();
      const data = {
        name: '',
        url: '',
      };
      return this.$http.post(url, data);
    },
    retrieveIdentities() {
      const url = window.Urls['api:identity-list']();
      return this.$http.get(url);
    },
    updateIdentity(identity) {
      const url = window.Urls['api:identity-detail'](identity.id);
      const data = identity;
      return this.$http.put(url, data);
    },
    deleteIdentity(identity) {
      const url = window.Urls['api:identity-detail'](identity.id);
      return this.$http.delete(url);
    },
  },
};
</script>

<style>
.sortable-chosen {
  opacity: 0;
}
.sortable-drag {
  opacity: 1;
}
</style>
