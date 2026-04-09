<template>
  <section class="flex p-4 items-center justify-center">
    <div class="w-85 max-w-md px-6 lg:w-150">
      <form
        @submit.prevent=""
        class="bg-white shadow-xl rounded-2xl p-8 flex flex-col gap-6"
      >
        <h2 class="text-2xl font-bold text-center text-gray-700">Registro</h2>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Apodo</label>
          <input type="text" class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition" v-model="apodo" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Email</label>
          <input type="email" class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition" v-model="email_user" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Contraseña</label>
          <input type="password" class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition" v-model="password_user" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-600">Repetir contraseña</label>
          <input type="password" class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition" v-model="password_user_confirm" />
        </div>

        <ButtonsLoginRegister
          content="REGISTRARME"
          class="mt-4 w-45 self-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
          @click="do_register"
        />

        <router-link to="/login">¿Ya tienes cuenta? <span class="text-[#ff5252]">Inicia sesión</span></router-link>
      </form>
    </div>
  </section>
</template>

<script setup>
import ButtonsLoginRegister from '@/components/ButtonsLoginRegister.vue';
import { ref } from 'vue';
import axios from 'axios';
import { useToast } from "vue-toastification";
import { useRouter } from 'vue-router';

const toast = useToast()
const router = useRouter()
let apodo = ref("")
let email_user = ref("")
let password_user = ref("")
let password_user_confirm = ref("")

const do_register = async () => {
  const clean = str => str.replace(/<[^>]*>?/gm, '')

  if(password_user.value !== password_user_confirm.value){
    toast.error("LAS CONTRASEÑAS DEBEN COINCIDIR")
    return
  }

  try {
    const response = await axios.post("/auth/register", {
      email: clean(email_user.value),
      name: clean(apodo.value),
      password: password_user.value,
      password_check: password_user_confirm.value
    }) // Se eliminó withCredentials

    if(response.status === 201 || response.status === 200){
      toast.success("Usuario registrado correctamente")
      localStorage.setItem("TOKEN", response.data.token)
      localStorage.setItem("USER_ID", response.data.user)
      router.push("/home")
    }
  } catch(error) {
    if(error.response){
      // Mostrar el error exacto del backend (ej. contraseña débil o email duplicado)
      const msg = error.response.data.error || "Error al registrar"
      toast.error(msg)
    } else {
      toast.error("Error interno del servidor ;(")
    }
  }
}
</script>