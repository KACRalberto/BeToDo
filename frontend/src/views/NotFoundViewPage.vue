<template>
  <div class="min-h-[85vh] w-full bg-zinc-50 flex flex-col items-center justify-center font-['Inter',_sans-serif] antialiased p-6">
    <div class="text-center">
      <div class="relative inline-block">
        <h1 class="text-9xl font-extrabold text-zinc-200 font-['Poppins',_sans-serif] tracking-widest">404</h1>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-6xl animate-bounce">🍅</span>
        </div>
      </div>
      
      <h2 class="text-3xl md:text-4xl font-bold text-zinc-800 mt-4 mb-3 font-['Poppins',_sans-serif]">¡Página no encontrada!</h2>
      <p class="text-lg text-zinc-600 max-w-md mx-auto mb-8">
        Parece que te has perdido. La página que buscas no existe o ha sido movida de lugar. ¡Tómate un breve descanso y vuelve al inicio!
      </p>
      
      <router-link 
        to="/" 
        class="inline-block bg-red-500 text-white font-bold text-lg py-3 px-8 rounded-xl shadow-[5px_5px_0px_#000] border-2 border-black hover:bg-white hover:text-red-500 hover:shadow-[5px_5px_0px_#ff5252] transition-all duration-300"
      >
        Volver al Inicio
      </router-link>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');
</style>