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
    <DraggableList v-model="aliases" @reordered="reorder">
      <template v-slot:listItems="eventListeners">
        <Alias
          v-for="(alias, index) in aliases"
          :key="alias.id"
          :alias="alias"
          :index="index"
          :disabled="alias.disabled"
          @moved="eventListeners.moved"
          @destroy="destroy"
        />
      </template>
    </DraggableList>
    <AddButton @create="create" aria-label="Add alias" />
  </form>
</template>

<script>
import Alias from '@/components/Alias.vue';
import AddButton from '@/components/AddButton.vue';
import DraggableList from '@/components/DraggableList.vue';

export default {
  name: 'AliasForm',
  components: {
    Alias,
    AddButton,
    DraggableList,
  },
  data() {
    return {
      aliases: [],
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
</style>
