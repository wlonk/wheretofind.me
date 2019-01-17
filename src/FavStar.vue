<template>
  <button
    class="favstar btn btn-outline-warning"
    :class="{ active: isActive }"
    @click="toggleFavstar"
  >
    <span class="fas fa-star"></span>
  </button>
</template>

<script>
export default {
  name: 'FavStar',
  props: {
    active: {
      type: Boolean,
      default: false,
    },
    username: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      isActive: this.active,
    };
  },
  methods: {
    toggleFavstar() {
      const originalActive = this.isActive;
      this.isActive = !originalActive;
      if (originalActive) {
        this.unfollow().catch(() => {
          this.isActive = originalActive;
        });
      } else {
        this.follow().catch(() => {
          this.isActive = originalActive;
        });
      }
    },
    unfollow() {
      const url = window.Urls['api:follow-detail'](this.username);
      return this.$http.delete(url);
    },
    follow() {
      const url = window.Urls['api:follow-list']();
      const data = {
        to_user: this.username,
      };
      return this.$http.post(url, data);
    },
  },
};
</script>

<style></style>
