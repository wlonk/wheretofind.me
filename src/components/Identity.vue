<template>
  <div class="identity draggable-item card bg-light shadow-sm w-100 mb-3">
    <div class="card-body">
      <div class="form-group row">
        <label :for="nameLabel" class="col-sm-2 col-form-label">Name</label>
        <div class="col-sm-9">
          <input
            type="text"
            class="form-control"
            name="name"
            :tabindex="nameTabIndex"
            v-model="identity.name"
            @change="update"
            @keyup.enter="update"
            :id="nameLabel"
            :disabled="disabled"
            placeholder="My blog…"
          />
        </div>
        <div class="col-sm-1 mt-2 mt-sm-0">
          <button
            type="button"
            class="btn btn-outline-danger float-right"
            :tabindex="destroyTabIndex"
            @click="destroy"
            aria-label="Remove identity"
          >
            <span class="fas fa-minus-circle"></span>
          </button>
        </div>
      </div>
      <div class="form-group row">
        <label :for="urlLabel" class="col-sm-2 col-form-label">Address</label>
        <div class="col-sm-9">
          <input
            type="text"
            class="form-control"
            name="url"
            :tabindex="urlTabIndex"
            v-model="identity.url"
            @change="updateUrl"
            @keyup.enter="updateUrl"
            :id="urlLabel"
            :disabled="disabled"
            placeholder="https://example.com/"
          />
        </div>
        <div class="col-sm-1">
          <button
            type="button"
            class="btn btn-link float-right expand-identity"
            :tabindex="expandTabIndex"
            @click="toggleExpanded"
            aria-label="Expand identity"
          >
            <span class="fas fa-ellipsis-h"></span>
          </button>
        </div>
      </div>
      <div :class="{ 'd-none': !expandExtras }">
        <div class="form-group row">
          <label :for="tagLabel" class="col-sm-2 col-form-label">Tag</label>
          <div class="col-sm-9">
            <input
              type="text"
              class="form-control"
              @change="update"
              @keyup.enter="update"
              v-model="identity.tag"
              :tabindex="tagTabIndex"
              :id="tagLabel"
            />
          </div>
        </div>
        <div class="form-group row">
          <label :for="qualityLabel" class="col-sm-2 col-form-label"
            >Signal</label
          >
          <div class="col-sm-9">
            <select
              class="custom-select"
              v-model.number="identity.quality"
              @change="update"
              :tabindex="qualityTabIndex"
              :id="qualityLabel"
            >
              <option value="0">Low</option>
              <option value="1">Mid</option>
              <option value="2">High</option>
            </select>
          </div>
          <div class="col-sm-1">
            <button
              type="button"
              class="btn btn-link float-right quality-preview-wrapper"
              @click="clickQuality"
              aria-label="Toggle signal"
            >
              <img
                :src="qualityPreview"
                :alt="qualityPreview"
                class="quality-preview"
              />
            </button>
          </div>
        </div>
        <div class="form-group row">
          <label :for="iconLabel" class="col-sm-2 col-form-label">Icon</label>
          <div class="col-sm-9">
            <select
              class="custom-select"
              v-model="identity.icon"
              @change="update"
              :tabindex="iconTabIndex"
              :id="iconLabel"
            >
              <option value="fas fa-link">web</option>
              <option value="fas fa-envelope">email</option>
              <option value="fab fa-angellist">AngelList</option>
              <option value="fab fa-behance">Behance</option>
              <option value="fab fa-bitbucket">Bitbucket</option>
              <option value="fab fa-codepen">Codepen</option>
              <option value="fab fa-deviantart">Deviantart</option>
              <option value="fab fa-diaspora">Diaspora</option>
              <option value="fab fa-discord">Discord</option>
              <option value="fab fa-dribbble">Dribbble</option>
              <option value="fab fa-ello">Ello</option>
              <option value="fab fa-etsy">Etsy</option>
              <option value="fab fa-facebook">Facebook</option>
              <option value="fab fa-github">GitHub</option>
              <option value="fab fa-gitlab">Gitlab</option>
              <option value="fab fa-goodreads">Goodreads</option>
              <option value="fab fa-google-plus-g">Google Plus</option>
              <option value="fab fa-instagram">Instagram</option>
              <option value="fab fa-keybase">Keybase</option>
              <option value="fab fa-kickstarter">Kickstarter</option>
              <option value="fab fa-lastfm">Last</option>
              <option value="fab fa-linkedin">LinkedIn</option>
              <option value="fab fa-mastodon">Mastodon</option>
              <option value="fa fa-matrix-org">Matrix</option>
              <option value="fab fa-medium">Medium</option>
              <option value="fab fa-patreon">Patreon</option>
              <option value="fab fa-paypal">Paypal</option>
              <option value="fab fa-pinterest">Pinterest</option>
              <option value="fa fa-pixelfed">Pixelfed</option>
              <option value="fab fa-ravelry">Ravelry</option>
              <option value="fab fa-reddit">Reddit</option>
              <option value="fab fa-skype">Skype</option>
              <option value="fab fa-slack">Slack</option>
              <option value="fab fa-snapchat">Snapchat</option>
              <option value="fab fa-soundcloud">Soundcloud</option>
              <option value="fab fa-stack-overflow">Stack Overflow</option>
              <option value="fab fa-steam">Steam</option>
              <option value="fab fa-teamspeak">Teamspeak</option>
              <option value="fab fa-telegram-plane">Telegram</option>
              <option value="fab fa-tumblr">Tumblr</option>
              <option value="fab fa-twitch">Twitch</option>
              <option value="fab fa-twitter">Twitter</option>
              <option value="fab fa-untappd">Untappd</option>
              <option value="fab fa-vimeo">Vimeo</option>
              <option value="fab fa-youtube">YouTube</option>
            </select>
          </div>
          <div class="col-sm-1">
            <button
              type="button"
              class="btn btn-link float-right"
              aria-label="Preview icon"
            >
              <span :class="identity.icon"></span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <DragHandle :itemIndex="index" :tabIndex="moveTabIndex" />
  </div>
</template>

<script>
import iconGuesses from '../iconGuesses';
import DragHandle from '@/components/DragHandle.vue';

export default {
  name: 'Identity',
  props: ['identity', 'disabled', 'index'],
  components: { DragHandle },
  data() {
    return {
      expandExtras: false,
    };
  },
  computed: {
    nameLabel() {
      return `name-${this.identity.id}`;
    },
    urlLabel() {
      return `url-${this.identity.id}`;
    },
    tagLabel() {
      return `tag-${this.identity.id}`;
    },
    qualityLabel() {
      return `quality-${this.identity.id}`;
    },
    iconLabel() {
      return `icon-${this.identity.id}`;
    },
    nameTabIndex() {
      return this.index * 10 + 2;
    },
    urlTabIndex() {
      return this.index * 10 + 3;
    },
    expandTabIndex() {
      return this.index * 10 + 4;
    },
    tagTabIndex() {
      return this.index * 10 + 5;
    },
    qualityTabIndex() {
      return this.index * 10 + 6;
    },
    iconTabIndex() {
      return this.index * 10 + 7;
    },
    destroyTabIndex() {
      return this.index * 10 + 8;
    },
    moveTabIndex() {
      return this.index * 10 + 9;
    },
    qualityPreview() {
      // TODO: This shouldn't involve explicit use of the /static/ directory.
      switch (this.identity.quality) {
        case 0:
          return ['/static/images/quality-low.svg'];
        case 1:
          return ['/static/images/quality-mid.svg'];
        case 2:
          return ['/static/images/quality-high.svg'];
      }
      return [];
    },
  },
  methods: {
    clickQuality() {
      this.identity.quality = (this.identity.quality + 1) % 3;
      this.update();
    },
    toggleExpanded() {
      this.expandExtras = !this.expandExtras;
    },
    guessIcon() {
      let icon;
      iconGuesses.forEach(el => {
        const { fn, val } = el;
        if (fn(this.identity.url)) {
          icon = val;
        }
      });
      this.identity.icon = icon;
    },
    updateUrl() {
      this.guessIcon();
      this.update();
    },
    update() {
      const url = window.Urls['api:identity-detail'](this.identity.id);
      const data = this.identity;
      const req = this.$http.put(url, data);
      // emit the Promise created by the $http call so that the state of the request can be tracked if so desired
      this.$emit('request-started', req);
      return req;
    },
    destroy() {
      // TODO flash "deleting" div.
      this.$emit('destroy', this.identity);
    },
  },
};
</script>

<style scoped>
.identity {
  background: url('../images/draghandle-right.png') no-repeat bottom 2px right
    3px;
}
.expand-identity:focus {
  box-shadow: 0 0 0 0.2rem rgba(120, 194, 173, 0.25);
}
.quality-preview {
  height: 1rem;
}
.quality-preview-wrapper {
  cursor: pointer;
  margin-right: -0.25rem;
}
.card-control-icon {
  bottom: 0;
  cursor: grab;
  height: 30px;
  position: absolute;
  right: 0;
  width: 30px;
}
.edit-button:focus {
  box-shadow: 0 0 0 0.2rem rgba(120, 194, 173, 0.25);
}
</style>
