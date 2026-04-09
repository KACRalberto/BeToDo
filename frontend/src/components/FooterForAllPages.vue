<template>
  <footer class="h-18 w-full bg-[#3A3A3A] flex justify-between items-center px-4">
    <div class="flex items-center gap-2">
      <span class="header-text"><router-link to="/">© BeToDo</router-link></span>
    </div>
    <div class="text-white">
        <ul class="flex">
          <li><a href="#"><i class="fa-brands fa-github text-3xl"></i></a></li>
          <li><a href="#"><i class="fa-brands fa-linkedin text-3xl"></i></a></li>
        </ul>
    </div>
  </footer>
</template>

<script setup>

</script>

<style lang="sass" scoped>
$color_header: #E4BB97
$color_1:#FEF5EF
$color_2:#D6E3F8
$color_3:#9D5C63
$color_4:#584B53

#menu-btn
  padding: 1px 2px
  font-size: 24px
  font-weight: bold
  text-align: center
  text-decoration: none
  color: #fff
  background-color: #ff5252
  border: 2px solid #000
  border-radius: 10px
  box-shadow: 5px 5px 0px #000
  transition: all 0.3s ease
  cursor: pointer
  outline: none

  svg
    width: 1.5rem
    height: 1.5rem

  &:hover
    background-color: #fff
    color: #ff5252
    border: 2px solid #ff5252
    box-shadow: 5px 5px 0px #ff5252

  &:active
    background-color: #fcf414
    box-shadow: none
    transform: translateY(4px)

.header-text
  font-family: "Righteous", sans-serif
  font-size: 24px
  color: white
  letter-spacing: 0.05em


.header-text a
  transition: color 0.5s ease-in-out
  &:hover
    color: #ff5252
</style>
