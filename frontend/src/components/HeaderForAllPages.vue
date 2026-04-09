<template>
  <header class="h-18 w-full bg-[#2D2D34] flex justify-between items-center px-4" id="BETO">
    <div class="flex items-center gap-2">
      <div class="w-15 rounded-[100%]">
        <img src="../assets/IMG/TOMATOBETO.png" alt="" class="h-full" />
      </div>
      <span class="header-text lg:flex hidden md:flex"><router-link to="/">BeToDo</router-link></span>
    </div>
    <nav
      class="flex-1 hidden lg:flex justify-center self-center text-[16px] font-[Righteous] text-white"
    >
      <ul class="flex gap-5">
        <li>
          <router-link
            to="/"
            :class="[{ 'text-[#ff5252] font-bold': route.path === '/' }, 'transition ease-in-out duration-500 delay-100 hover:text-[#ff5252]']"
          >
            Inicio
          </router-link>
        </li>
        <li>
          <router-link
            to="/services"
            :class="[{ 'text-[#ff5252] font-bold': route.path === '/services' }, 'transition ease-in-out duration-500 delay-100 hover:text-[#ff5252]']"
          >
            Servicios
          </router-link>
        </li>
        <li>
          <router-link
            to="/about"
            :class="[{ 'text-[#ff5252] font-bold': route.path === '/about' }, 'transition ease-in-out duration-500 delay-100 hover:text-[#ff5252]']"
          >
            Nosotros
          </router-link>
        </li>
        <li>
          <router-link
            to="/contact"
            :class="[{ 'text-[#ff5252] font-bold': route.path === '/contact' }, 'transition ease-in-out duration-500 delay-100 hover:text-[#ff5252]']"
          >
            Contacto
          </router-link>
        </li>
      </ul>
    </nav>
    <nav class="self-center p-2 z-4">
      <transition
        enter-active-class="animate__animated animate__fadeInLeft"
        leave-active-class="animate__animated animate__fadeOutLeft"
      >
        <div
          v-if="menu_mostrado"
          id="menu"
          class="lg:hidden absolute left-0 my-9 text-center w-full"
        >
          <ul class="flex flex-col">
            <li
              class="h-15 flex items-center justify-center bg-[#B8BDB5] animate__animated animate__fadeInLeft group hover:bg-[#DCE3E8]"
              style="animation-delay: 0s"
            >
              <router-link
                to="/"
                class="block w-full"
                :class="[{ 'font-[900] text-[#ff5252] bg-[#DCE3E8]': route.path === '/' }, 'group-hover:font-[900]']"
              >
                Inicio
              </router-link>
            </li>
            <li
              class="h-15 flex items-center justify-center bg-[#B8BDB5] animate__animated animate__fadeInLeft group hover:bg-[#DCE3E8]"
              style="animation-delay: 0.2s"
            >
              <router-link
                to="/services"
                class="block w-full"
                :class="[{ 'font-[900] text-[#ff5252] bg-[#DCE3E8]': route.path === '/services' }, 'group-hover:font-[900]']"
              >
                Servicios
              </router-link>
            </li>
            <li
              class="h-15 flex items-center justify-center bg-[#B8BDB5] animate__animated animate__fadeInLeft group hover:bg-[#DCE3E8]"
              style="animation-delay: 0.4s"
            >
              <router-link
                to="/about"
                class="block w-full"
                :class="[{ 'font-[900] text-[#ff5252] bg-[#DCE3E8]': route.path === '/about' }, 'group-hover:font-[900]']"
              >
                Nosotros
              </router-link>
            </li>
            <li
              class="h-15 flex items-center justify-center bg-[#B8BDB5] animate__animated animate__fadeInLeft group hover:bg-[#DCE3E8]"
              style="animation-delay: 0.6s"
            >
              <router-link
                to="/contact"
                class="block w-full"
                :class="[{ 'font-[900] text-[#ff5252] bg-[#DCE3E8]': route.path === '/contact' }, 'group-hover:font-[900]']"
              >
                Contacto
              </router-link>
            </li>
          </ul>
        </div>
      </transition>
    </nav>

    <div class="flex gap-4 pr-4 self-center">
        <button
        id="menu-btn"
        class="lg:hidden focus:outline-none"
        @click="mostrar_menu"
      >
        <svg class="w-6 h-6" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      
      <!-- Solo mostrar si NO está logueado -->
      <template v-if="!isLoggedIn">
        <router-link to="/login">
          <ButtonsLoginRegister content="LOGIN"></ButtonsLoginRegister>
        </router-link>
        <router-link to="/register">
          <ButtonsLoginRegister content="REGISTER"></ButtonsLoginRegister>
        </router-link>
      </template>

    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import ButtonsLoginRegister from './ButtonsLoginRegister.vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
let menu_mostrado = ref(false)
const isLoggedIn = ref(!!localStorage.getItem("TOKEN"))

// Actualizar isLoggedIn cada vez que se navega
router.afterEach(() => {
  isLoggedIn.value = !!localStorage.getItem("TOKEN")
})

const mostrar_menu = () => {
  menu_mostrado.value = !menu_mostrado.value
}
</script>

<style lang="sass" scoped>
$color_header: #E4BB97
$color_1:#FEF5EF
$color_2:#D6E3F8
$color_3:#9D5C63
$color_4:#584B53

header
    z-index: 999

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
