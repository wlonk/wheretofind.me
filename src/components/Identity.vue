<template>
  <div
    class="identity card bg-light shadow-sm w-100 mb-3"
    :class="editing ? 'flex-sm-row' : 'flex-row'"
    style="justify-content:space-between;"
  >
    <button
      aria-label="Edit identity"
      class="btn btn-link edit-button"
      :tabindex="editButtonTabIndex"
      @click="editing = !editing"
    >
      <i
        class="fas"
        :class="editing ? 'fa-caret-square-up' : 'fa-pencil-alt'"
      ></i>
    </button>
    <div v-if="editing" class="card-body flex-column">
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
              <option value="fab fa-mastodon">Mastodon</option>
              <option value="fab fa-medium">Medium</option>
              <option value="fab fa-patreon">Patreon</option>
              <option value="fab fa-paypal">Paypal</option>
              <option value="fab fa-pinterest">Pinterest</option>
              <option value="fab fa-ravelry">Ravelry</option>
              <option value="fab fa-reddit">Reddit</option>
              <option value="fab fa-skype">Skype</option>
              <option value="fab fa-slack">Slack</option>
              <option value="fab fa-snapchat">Snapchat</option>
              <option value="fab fa-soundcloud">Soundcloud</option>
              <option value="fab fa-stackoverflow">Stackoverflow</option>
              <option value="fab fa-steam">Steam</option>
              <option value="fab fa-teamspeak">Teamspeak</option>
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
    <div style="display:flex;align-self:center;" v-if="!editing">
      {{ identity.name }}
    </div>
    <div
      @keydown.prevent.stop.up.down="rearrangeSelf"
      :tabIndex="moveTabIndex"
      class="card-control-icon rearrange-handle"
      ref="rearrangeHandle"
    >
      <i class="fas fa-arrows-alt fa-lg"></i>
    </div>
  </div>
</template>

<script>
import iconGuesses from '../iconGuesses';

export default {
  name: 'Identity',
  props: ['identity', 'disabled', 'index'],
  data() {
    return {
      expandExtras: false,
      editing: this.identity.new,
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
    editButtonTabIndex() {
      return this.index * 10 + 1;
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
    rearrangeSelf(e) {
      const eventObject = {
        index: this.index,
        handle: this.$refs.rearrangeHandle, // needed so that the form can keep the handle in focus after rearranging things
        el: this.$el, // needed so that the form can monitor whether this identity's html element is still in view or not
      };
      if (e.keyCode === 38) {
        eventObject.direction = 'up';
        this.$emit('moved', eventObject);
      } else if (e.keyCode === 40) {
        eventObject.direction = 'down';
        this.$emit('moved', eventObject);
      }
    },
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
      return this.$http.put(url, data);
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
  background: url('../images/draghandle.png') no-repeat bottom 2px left 3px;
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
  display: flex;
  padding: 1.25rem 0.75rem 1.25rem 0.75rem;
  height: fit-content;
  align-self: center;
}
@media screen and (max-width: 576px) {
  .card-control-icon {
    padding: 0.75rem;
  }
}
.rearrange-handle {
  cursor: grab;
}
.edit-button:focus {
  box-shadow: 0 0 0 0.2rem rgba(120, 194, 173, 0.25);
}
</style>
