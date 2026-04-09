<template>
  <section class="w-full flex flex-col bg-zinc-50 font-['Inter',_sans-serif] antialiased text-zinc-900 overflow-hidden">
    <!-- HERO SECTION -->
    <div 
      class="relative flex flex-col items-center justify-center w-full min-h-[85vh] p-6 lg:p-10 bg-cover bg-center"
      style="background-image: linear-gradient(rgba(254, 245, 239, 0.8), rgba(254, 245, 239, 0.8)), url('@/assets/IMG/FNDO.png');"
    >
      <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-center tracking-tight text-zinc-900 mb-4 animate__animated animate__fadeInDown font-['Poppins',_sans-serif]">
        ORGANIZA TU DÍA, <br class="hidden sm:block">
        <span class="text-red-500">PLANIFICA SIN ESTRÉS</span>
      </h1>
      
      <p class="text-lg md:text-xl font-medium text-zinc-700 max-w-2xl text-center mb-10 animate__animated animate__fadeInUp">
        BeToDo organiza tus tareas diarias, proyectos y recordatorios en un solo lugar. 
        Planifica, prioriza y completa objetivos fácilmente con una app simple y confiable.
      </p>

      <router-link 
        to="/register" 
        class="bg-red-500 text-white font-bold text-xl py-4 px-10 rounded-xl border-2 border-black shadow-[5px_5px_0px_#000] hover:bg-white hover:text-red-500 hover:border-red-500 hover:shadow-[5px_5px_0px_#ff5252] active:bg-yellow-400 active:shadow-none active:translate-y-1 transition-all duration-300 animate__animated animate__zoomIn"
      >
        ¿Comenzamos?
      </router-link>
      
      <router-link to="/login" class="mt-6 text-zinc-600 font-semibold hover:text-zinc-900 transition animate__animated animate__fadeIn">
        ¿Ya tienes cuenta? <span class="text-blue-600 font-bold hover:underline">Inicia sesión.</span>
      </router-link>
    </div>

    <!-- POMODORO INFO SECTION -->
    <div class="w-full max-w-6xl mx-auto flex flex-col lg:flex-row items-center justify-between py-16 px-6 lg:px-10 gap-10">
      <img class="rounded-2xl shadow-xl w-full max-w-md lg:max-w-lg object-cover transform hover:scale-105 transition duration-500" src="../assets/IMG/PNGPORTATIL.png" alt="Pomodoro Laptop">
      <div class="flex flex-col max-w-xl">
        <h2 class="text-3xl font-bold text-red-500 mb-4 font-['Poppins',_sans-serif]">Técnica Pomodoro</h2>
        <p class="text-lg text-zinc-700 leading-relaxed mb-4">
          Es un método de estudio que divide el tiempo en bloques de 25 minutos de concentración, seguidos de breves descansos.
        </p>
        <p class="text-lg text-zinc-700 leading-relaxed">
          Ayuda a mejorar el enfoque, evitar distracciones y estudiar de forma más eficiente y sostenible.
        </p>
      </div>
    </div>
        
    <!-- FEATURES SECTION -->
    <div class="w-full bg-zinc-100 py-16 px-6 lg:px-10">
      <div class="max-w-6xl mx-auto flex flex-col-reverse lg:flex-row items-center justify-between gap-10">
        <div class="flex flex-col max-w-2xl text-center lg:text-left">
          <h2 class="text-3xl font-bold text-zinc-900 mb-4 font-['Poppins',_sans-serif]">Integrado en <span class="text-red-500">BeToDo</span></h2>
          <p class="text-lg text-zinc-700 leading-relaxed">
            Cada tarea puede gestionarse siguiendo la técnica Pomodoro. Solo elige una tarea, activa los bloques de 25 minutos de enfoque y 5 minutos de descanso, y aprovecha tu tiempo de manera más eficiente. ¡Tú decides cuándo y cómo usar 
            <span class="text-red-500 font-bold">Pomodoro</span>! 🍅
          </p>
        </div>
        <img src="../assets/IMG/TOMATOBETO.png" class="w-40 lg:w-56 drop-shadow-lg animate-bounce-slow" alt="Tomato Mascot">
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
let valor = ref(false);
onMounted(() => {
  setTimeout(() => {
    valor.value = true;
  }, 500);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');

.animate-bounce-slow {
  animation: bounce 3s infinite;
}
</style>
