<template>
  <section class="flex flex-1 items-center justify-center p-4">
    <div class="w-full max-w-5xl flex flex-col md:flex-row  rounded-2xl overflow-hidden shadow-2xl">
      <form
        @submit.prevent=""
        class="bg-white w-full md:w-1/2 p-6 md:p-8 flex flex-col gap-6 rounded-tl-2xl rounded-bl-2xl"
      >
        <h2 class="text-2xl font-semibold text-center text-gray-700">
          Inicio de sesión
        </h2>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Email</label>
          <input
            type="email"
            class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            v-model="email_login"
          />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Contraseña</label>
          <input
            type="password"
            class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            v-model="password_login"
          />
        </div>

        <ButtonsLoginRegister
          content="INICIAR SESIÓN"
          class="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
          @click="do_login"
        />

        <router-link class="text-center mt-2 text-gray-600" to="/register">
          ¿Aún no tienes cuenta? 
          <span class="text-[#ff5252] font-semibold">Regístrate</span>
        </router-link>
        <router-link class="text-center mt-2 text-gray-600" to="/forgot-password">
          <span class="text-sm text-[#ff5252]">¿Olvidaste tu contraseña?</span>
        </router-link>
      </form>

      <div class="w-full md:w-1/2 flex flex-col justify-center items-center text-center p-6 md:p-8 bg-[#ff7a7a]">
        <h1 class="mb-3 font-[Poppins] text-lg md:text-xl font-bold text-white">
          ¡Bienvenido de nuevo!
        </h1>
        <p class="font-[Poppins] text-[14px] md:text-[16px] font-semibold text-white">
          Nos alegra verte otra vez por aquí. Inicia sesión para continuar, acceder a tu cuenta y seguir disfrutando de BeToDo.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import ButtonsLoginRegister from '@/components/ButtonsLoginRegister.vue';
import { ref } from 'vue';
import axios from 'axios';
import { useToast } from "vue-toastification";
import { useRouter } from 'vue-router';

const router = useRouter()
let email_login = ref("")
let password_login = ref("")
const toast = useToast()

const do_login = async () => {
  try {
    const clean = str => str.replace(/<[^>]*>?/gm, '')
    const response = await axios.post("/auth/login", {
      email: clean(email_login.value),
      password: password_login.value
    }) // Se eliminó withCredentials

    if(response.status === 200){
      toast.success("Todo correcto")
      // GUARDAMOS EL TOKEN JWT
      localStorage.setItem("TOKEN", response.data.token)
      localStorage.setItem("USER_ID", response.data.user)
      router.push("/home")
    }

  } catch(error) {
    if(error.response){
      if(error.response.status === 400){
        toast.error("EMAIL Y CONTRASEÑA REQUERIDOS")
      } else if(error.response.status == 401){
        toast.error("Email o contraseña incorrectos")
      } else {
        toast.error("Error interno del servidor ;(")
      }
    }
  }
}
</script>