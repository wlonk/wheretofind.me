<template>
  <button
    @click="showSaveAnimation"
    class="btn btn-outline-primary float-left"
    v-bind:disabled="!allRequestsComplete"
  >
    Save
    <i
      v-if="spinning"
      class="fas fa-spinner inline-status-display spinning"
    ></i>
    <transition name="spin">
      <i v-if="!spinning" class="fas fa-check inline-status-display"></i>
    </transition>
  </button>
</template>

<script>
export default {
  data() {
    return {
      animatingDueToClick: false,
    };
  },
  props: {
    allRequestsComplete: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    spinning() {
      // making Absolutely Sure that both of these are accessed and thus registered as dependencies for the property, despite short-circuit evaluation
      const a = !this.allRequestsComplete;
      const b = this.animatingDueToClick;
      return a || b;
    },
  },
  methods: {
    showSaveAnimation() {
      if (this.allRequestsComplete) {
        this.animatingDueToClick = true;
        setTimeout(() => {
          this.animatingDueToClick = false;
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

.spinning {
  animation: spin 0.75s infinite linear;
}

/* used by the "spin" transition element */
.spin-enter-active {
  animation: spin 0.75s ease-out;
}
.spin-leave-active {
  display: none;
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
