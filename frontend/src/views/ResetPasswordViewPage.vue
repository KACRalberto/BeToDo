<template>
  <div class="w-full max-w-md mx-auto p-6 mt-10">
    <h1 class="text-2xl font-bold mb-4 text-center">Restablecer contraseña</h1>

    <form @submit.prevent="handleReset" class="bg-white p-6 rounded shadow flex flex-col gap-4">
      <div v-if="!token" class="bg-red-100 text-red-700 p-3 rounded-lg text-sm text-center font-semibold">
        Enlace inválido. Faltan credenciales de recuperación en la URL.
      </div>

      <div class="flex flex-col gap-1">
        <label class="block text-sm font-medium mb-1">Nueva contraseña</label>
        <input v-model="password" type="password" class="w-full border rounded px-3 py-2" required :disabled="!token" />
        <span class="text-xs text-gray-500">Mínimo 8 caracteres y al menos un número.</span>
      </div>

      <div class="flex flex-col gap-1">
        <label class="block text-sm font-medium mb-1">Confirmar contraseña</label>
        <input v-model="password2" type="password" class="w-full border rounded px-3 py-2" required :disabled="!token" />
      </div>

      <div class="text-right mt-4">
        <button type="submit" class="bg-[#ff5252] text-white px-4 py-2 rounded disabled:bg-gray-400" :disabled="!token || isLoading">
          {{ isLoading ? 'Guardando...' : 'Cambiar contraseña' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const token = route.query.token || ''
const password = ref('')
const password2 = ref('')
const isLoading = ref(false)

async function handleReset(){
  if(!token) return toast.error('Token de recuperación no válido')
  if(password.value !== password2.value) return toast.error('Las contraseñas no coinciden')

  const regexNumero = /\d/
  if(password.value.length < 8 || !regexNumero.test(password.value)){
    return toast.error('La contraseña debe tener al menos 8 caracteres y un número')
  }

  isLoading.value = true
  try{
    const resp = await axios.post('reset-password', { 
      token: token, 
      password: password.value 
    })
    if(resp.status === 200){
      toast.success('Contraseña actualizada. Ya puedes iniciar sesión.')
      router.push('/login')
    }
  }catch(err){
    const errorMsg = err.response?.data?.error || 'Error al restablecer la contraseña'
    toast.error(errorMsg)
  }finally{
    isLoading.value = false
  }
}
</script>