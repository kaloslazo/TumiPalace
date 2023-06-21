<!-- Router logic -->
<template>
  <div class="max-w-7xl mx-auto">
    <NavbarDefault v-if="!$route.meta.hideNavigation"/>
    <router-view />
  </div>
</template>


<!-- User views logic -->
<script>
import NavbarDefault from './components/NavbarDefault.vue'

export default {
  components: {
    NavbarDefault
  },
}
</script>


<style>
body, html {
  padding: 0;
  margin: 0;
  width: 100%;
  min-height: 100%;
  background-color: #3E312B;
}
</style>