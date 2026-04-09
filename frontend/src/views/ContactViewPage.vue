<template>
  <div class="min-h-[83vh] w-full bg-zinc-50 py-12 px-6 flex flex-col items-center justify-center font-['Inter',_sans-serif] antialiased">
    <header class="mb-10 text-center max-w-2xl">
      <h1 class="text-4xl md:text-5xl font-extrabold text-zinc-900 mb-4 font-['Poppins',_sans-serif]">Contacto</h1>
      <p class="text-lg text-zinc-600">¿Tienes preguntas o sugerencias? Escríbenos y nos pondremos en contacto contigo lo antes posible.</p>
    </header>

    <form @submit.prevent="handleSubmit" class="bg-white p-8 md:p-10 rounded-3xl shadow-xl border border-zinc-100 w-full max-w-2xl">
      <div class="mb-6">
        <label class="block text-sm font-semibold text-zinc-700 mb-2">Nombre</label>
        <input v-model="form.name" type="text" class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-500/50 transition-all" placeholder="Tu nombre" required />
      </div>

      <div class="mb-6">
        <label class="block text-sm font-semibold text-zinc-700 mb-2">Email</label>
        <input v-model="form.email" type="email" class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-500/50 transition-all" placeholder="tu@email.com" required />
      </div>

      <div class="mb-8">
        <label class="block text-sm font-semibold text-zinc-700 mb-2">Mensaje</label>
        <textarea v-model="form.message" rows="5" class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-500/50 transition-all resize-none" placeholder="¿En qué podemos ayudarte?" required></textarea>
      </div>

      <div class="flex justify-center">
        <button type="submit" class="w-full md:w-auto bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-10 rounded-xl shadow-lg shadow-red-500/30 transform hover:-translate-y-1 transition-all duration-300">
          Enviar Mensaje
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useToast } from 'vue-toastification'
import axios from 'axios'

const toast = useToast()
const form = reactive({ name: '', email: '', message: '' })

async function handleSubmit() {
  try {
    await axios.post('/auth/contact', {
      nombre: form.name,
      email: form.email,
      mensaje: form.message
    })
    toast.success('Mensaje enviado. Gracias por contactarnos.')
    form.name = ''
    form.email = ''
    form.message = ''
  } catch (error) {
    toast.error('Hubo un error al enviar el mensaje.')
    console.error('Error al enviar el contacto:', error)
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');
</style>
