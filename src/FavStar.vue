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
  name: "FavStar",
  props: {
    active: {
      type: Boolean,
      default: false
    },
    username: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      isActive: this.active
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
    // TODO: the API calls could live in a dedicated API component.
    // Extra so the URLs.
    unfollow() {
      const url = `/api/follows/${this.username}/`;
      const options = this.getFetchOptions({
        method: "DELETE"
      });
      return fetch(url, options);
    },
    follow() {
      const url = "/api/follows/";
      const data = {
        to_user: this.username
      };
      const options = this.getFetchOptions({
        method: "POST",
        body: JSON.stringify(data)
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
