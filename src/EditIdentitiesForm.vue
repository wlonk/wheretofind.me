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
// TODO: Support drag and drop, perhaps using
// https://github.com/SortableJS/Vue.Draggable
import Identity from "./components/Identity.vue";
import AddIdentityButton from "./components/AddIdentityButton.vue";
import draggable from "vuedraggable";

export default {
  name: "EditIdentitiesForm",
  components: {
    Identity,
    AddIdentityButton,
    draggable
  },
  props: {
    draggableOptions: {
      type: Object,
      default() {
        return {
          items: ".identity",
          axis: "y",
          containment: "parent"
        };
      }
    }
  },
  data() {
    return {
      identities: []
    };
  },
  created() {
    const url = "/api/identities/";
    const options = this.getFetchOptions({
      method: "GET"
    });
    // TODO: this approach has a flash as the original DOM elements are
    // replaced by the Vue ones.
    fetch(url, options)
      .then(r => r.json())
      .then(resp => {
        this.identities = resp;
      });
  },
  methods: {
    handleReorderIdentities() {
      const url = "/api/identities/reorder/";
      const data = this.identities.map(i => i.id);
      const options = this.getFetchOptions({
        method: "POST",
        body: JSON.stringify(data)
      });

      fetch(url, options).catch(() => {
        // TODO: revert to pre-sorted order.
      });
    },
    handleCreateIdentity() {
      const newIdentity = {
        id: this.identities.length + 1,
        name: "",
        url: "",
        disabled: true
      };
      this.identities.push(newIdentity);
      this.createNewIdentity()
        .then(r => r.json())
        .then(resp => {
          const { id } = resp;
          newIdentity.disabled = false;
          newIdentity.id = id;
        })
        // TODO: display error state.
        .catch();
    },
    handleUpdateIdentity(identity) {
      this.updateIdentity(identity)
        .then()
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
    // TODO: This is WET, copied from the FavStar component. We should move all
    // this into an API component and call it there.
    createNewIdentity() {
      const url = "/api/identities/";
      const data = {
        name: "",
        url: ""
      };
      const options = this.getFetchOptions({
        method: "POST",
        body: JSON.stringify(data)
      });
      return fetch(url, options);
    },
    updateIdentity(identity) {
      const url = `/api/identities/${identity.id}/`;
      const data = identity;
      const options = this.getFetchOptions({
        method: "PUT",
        body: JSON.stringify(data)
      });
      return fetch(url, options);
    },
    deleteIdentity(identity) {
      const url = `/api/identities/${identity.id}/`;
      const options = this.getFetchOptions({
        method: "DELETE"
      });
      return fetch(url, options);
    },
    getFetchOptions(merge) {
      return this.extend(
        {
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.$cookie.get("csrftoken")
          }
        },
        merge
      );
    },
    extend(obj, src) {
      Object.keys(src).forEach(key => {
        obj[key] = src[key];
      });
      return obj;
    }
  }
};
</script>

<style></style>
