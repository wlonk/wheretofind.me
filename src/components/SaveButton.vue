<template>
  <span>
    <button
      @click="showSaveAnimation"
      class="btn add-identity btn-outline-primary float-left"
    >
      Save
      <i
        key="checkmark"
        v-if="spinning"
        class="fas fa-spinner inline-status-display spin-quick-endless"
      ></i>
      <transition name="spin">
        <i
          key="spinner"
          v-if="!spinning"
          class="fas fa-check inline-status-display"
        ></i>
      </transition>
    </button>
  </span>
</template>

<script>
// if something is saving or the button's just been clicked, display the spinner; otherwise, display the checkmark
export default {
  data() {
    return {
      justBeenClicked: false,
    };
  },
  props: {
    allUploadsComplete: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    spinning() {
      return !this.allUploadsComplete || this.justBeenClicked; //TODO: figure out if justBeenClicked is monitored accurately for this
    },
  },
  methods: {
    showSaveAnimation() {
      if (this.allUploadsComplete) {
        this.justBeenClicked = true;
        setTimeout(() => {
          this.justBeenClicked = false;
        }, 400);
      }
    },
  },
};
</script>

<style scoped>
.inline-status-display {
  margin-left: 5px;
}

/* this makes double-extra-sure that Either the spinner or the checkmark is shown - Vue was rendering both briefly on my machine during the transition */
.inline-status-display:last-of-type:not(:first-of-type) {
  display: none;
}

.spin-quick-endless {
  animation: spin 1s infinite linear;
}

.spin-enter-active {
  animation: spin 0.5s linear;
}

@keyframes spin {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(359deg);
    transform: rotate(359deg);
  }
}
</style>
