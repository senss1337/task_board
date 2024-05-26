<template>
  <router-view :dark-mode="darkMode" @toggle-dark-mode="toggleDarkMode" />
</template>

<script>
export default {
  data() {
    return {
      darkMode: false
    };
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    }
  }
};
</script>

<style>
@import "https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css";
</style>
