<template>
  <div class="favstar">
    <div class="input-group dropright">
      <div :class="{ 'input-group-prepend': isActive }">
        <button
          type="button"
          class="btn btn-outline-warning"
          :class="{ 'btn-sm': small, active: isActive }"
          @click="toggleFavstar"
          aria-label="favstar"
        >
          <span class="fas fa-star"></span>
          <span
            v-if="isActive"
            class="pl-3"
            :class="[showNicknameField ? 'd-none' : '']"
            >{{ localNickname }}</span
          >
        </button>
      </div>
      <input
        v-model="localNickname"
        ref="nicknameField"
        type="text"
        class="form-control"
        :class="[showNicknameField ? '' : 'd-none']"
        placeholder="Nickname"
        @change="updateNickname"
        @keyup.enter="updateNickname"
        :focus="showNicknameField"
      />
      <div v-if="isActive" class="input-group-append">
        <button
          type="button"
          class="btn btn-warning dropdown-toggle dropdown-toggle-split"
          aria-haspopup="true"
          :aria-expanded="showNicknameField"
          @click="toggleShowNickname"
          aria-label="favstar expand"
        >
          <span class="sr-only">Toggle nickname field</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';

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
    small: {
      type: Boolean,
      default: false,
    },
    nickname: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      isActive: this.active,
      localNickname: this.nickname,
      showNicknameField: false,
    };
  },
  methods: {
    toggleShowNickname() {
      this.showNicknameField = !this.showNicknameField;
      return Vue.nextTick().then(() => {
        this.$refs.nicknameField.focus();
      });
    },
    toggleFavstar() {
      const originalActive = this.isActive;
      this.isActive = !originalActive;
      let callback;
      if (originalActive) {
        callback = this.unfollow;
      } else {
        callback = this.follow;
      }
      this.showNicknameField = false;
      callback().catch(() => {
        this.isActive = originalActive;
      });
    },
    unfollow() {
      const url = window.Urls['api:follow-detail'](this.username);
      return this.$http.delete(url);
    },
    follow() {
      const url = window.Urls['api:follow-list']();
      const data = {
        to_user: this.username,
        nickname: this.nickname,
      };
      return this.$http.post(url, data);
    },
    updateNickname() {
      const url = window.Urls['api:follow-detail'](this.username);
      const data = {
        nickname: this.localNickname,
      };
      this.$http.patch(url, data);
      this.showNicknameField = false;
    },
  },
};
</script>

<style lang="scss">
// Because this is absolutely positioned, you must put this component inside a
// postioned element, or it will jump elsewhere in the page. Be warned!
$spacer: 1rem;
.favstar {
  position: absolute;
  right: $spacer * 0.5;
  top: $spacer * 0.25;
  z-index: 10;
}
</style>
