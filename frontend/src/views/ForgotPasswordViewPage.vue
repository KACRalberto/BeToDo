<template>
  <div class="w-full max-w-2xl mx-auto p-6 mt-10">
    <h1 class="text-2xl font-bold mb-4">Recuperar contraseña</h1>

    <form @submit.prevent="handleRequest" class="bg-white p-6 rounded shadow">
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded px-3 py-2" required />
      </div>

      <div class="text-right">
        <button type="submit" class="bg-[#ff5252] text-white px-4 py-2 rounded">Enviar enlace de recuperación</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()
const email = ref('')

async function handleRequest(){
  try {
    const clean = str => str.replace(/<[^>]*>?/gm, '')
    // Solo enviamos la solicitud. El backend se encarga del correo.
    const resp = await axios.post('/auth/request-password-reset', { 
      email: clean(email.value) 
    })
    
    if(resp.status === 200){
      toast.success(resp.data.message || 'Si existe la cuenta, se ha enviado un correo.')
      email.value = ''
    }
  } catch(err) {
    console.error(err)
    toast.error('Error al solicitar recuperación')
  }
}
</script>