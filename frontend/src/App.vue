<script setup>
import FooterForAllPages from './components/FooterForAllPages.vue';
import HeaderForAllPages from './components/HeaderForAllPages.vue'
</script>


<template >

  <div class="flex flex-col min-h-screen">
    <HeaderForAllPages />
    <main class="flex-1 flex items-center justify-center">
      <router-view />
    </main>
    <FooterForAllPages class=""/>
  </div>

</template>

<style lang="sass" scoped>
main
  background-color: #B8BDB5
</style>

<style lang="sass">
/* Global scrollbar styles to match app colors */
:root
  --scroll-track: #2D2D34
  --scroll-thumb-start: #E4BB97
  --scroll-thumb-end: #ff5252

*::-webkit-scrollbar
  width: 12px
  height: 12px

*::-webkit-scrollbar-track
  background: var(--scroll-track)
  border-radius: 9999px

*::-webkit-scrollbar-thumb
  background: linear-gradient(180deg, var(--scroll-thumb-start), var(--scroll-thumb-end))
  border-radius: 9999px
  border: 3px solid var(--scroll-track)

*::-webkit-scrollbar-thumb:hover
  filter: brightness(0.95)

html
  scrollbar-width: thin
  scrollbar-color: var(--scroll-thumb-start) var(--scroll-track)
</style>
