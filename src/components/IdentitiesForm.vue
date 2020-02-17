<template>
  <form @submit.prevent class="clearfix">
    <draggable v-model="identities" :options="draggableOptions" @end="reorder">
      <Identity
        v-for="(identity, index) in identities"
        :key="identity.id"
        :identity="identity"
        :index="index"
        :disabled="identity.disabled"
        @destroy="destroy"
        @upload-started="startUpload"
      />
    </draggable>
    <SaveButton
      v-bind:allUploadsComplete="allUploadsComplete"
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
          axis: 'y',
          containment: 'parent',
          filter: 'input',
          preventOnFilter: false,
        };
      },
    },
  },
  data() {
    return {
      identities: [],
      runningUploads: 0,
    };
  },
  computed: {
    allUploadsComplete() {
      return this.runningUploads === 0;
    },
  },
  created() {
    // TODO: this approach has a flash as the original DOM elements are
    // replaced by the Vue ones.
    this.retrieveIdentities().then(resp => {
      this.identities = resp.data;
    });
  },
  methods: {
    // wraps Promises returned by $http methods so that the number of active uploads can be tracked; use for any request calls that the
    // user will want to see the status of by calling this.startUpload(this.$http.post/get/delete(...))
    startUpload(uploadRequestPromise) {
      this.runningUploads += 1;
      return uploadRequestPromise.then(this.finishUpload);
    },
    finishUpload(passThrough) {
      this.runningUploads -= 1;
      return passThrough;
    },

    reorder() {
      return (
        this.reorderIdentities()
          // TODO: revert to pre-sorted order on error.
          .catch()
      );
    },
    create() {
      const newId = Math.max.apply(Math, this.identities.map(i => i.id)) + 1;
      const newIdentity = {
        id: newId,
        name: '',
        url: '',
        quality: 2,
        icon: 'fas fa-link',
        disabled: true,
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
    // API calls:
    reorderIdentities() {
      const url = window.Urls['api:identity-reorder']();
      const data = this.identities.map(i => i.id);
      return this.startUpload(this.$http.post(url, data));
    },
    createNewIdentity() {
      const url = window.Urls['api:identity-list']();
      const data = {
        name: '',
        url: '',
      };
      return this.startUpload(this.$http.post(url, data));
    },
    retrieveIdentities() {
      const url = window.Urls['api:identity-list']();

      return this.$http.get(url);
    },
    destroyIdentity(identity) {
      const url = window.Urls['api:identity-detail'](identity.id);
      return this.startUpload(this.$http.delete(url));
    },
  },
};
</script>

<style scoped>
.sortable-drag {
  opacity: 1;
}
</style>
