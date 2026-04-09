<template>
  <div class="min-h-[83vh] w-full bg-zinc-50 py-12 px-6 flex items-center justify-center font-['Inter',_sans-serif] antialiased">
    <div class="max-w-5xl mx-auto bg-white rounded-3xl shadow-xl overflow-hidden border border-zinc-100">
      
      <header class="bg-gradient-to-r from-red-500 to-orange-500 p-10 text-center text-white">
        <h1 class="text-4xl md:text-5xl font-extrabold mb-4 drop-shadow-md font-['Poppins',_sans-serif]">Sobre Nosotros</h1>
        <p class="text-lg md:text-xl font-medium max-w-2xl mx-auto opacity-90">
          Somos un pequeño equipo dedicado a mejorar la productividad a través de herramientas sencillas, modernas y efectivas.
        </p>
      </header>
  
      <div class="p-10">
        <section class="mb-12 text-center">
          <h2 class="text-3xl font-bold text-zinc-800 mb-4 font-['Poppins',_sans-serif]">Nuestra Misión</h2>
          <p class="text-lg text-zinc-600 max-w-3xl mx-auto leading-relaxed">
            Facilitar la organización personal y de equipos, eliminando la fricción del día a día para ayudar a las personas a enfocarse plenamente en lo que realmente importa.
          </p>
        </section>
  
        <section>
          <h2 class="text-3xl font-bold text-zinc-800 mb-8 text-center font-['Poppins',_sans-serif]">El Equipo</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            <div class="p-8 bg-zinc-50 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 text-center flex flex-col items-center group">
              <div class="h-28 w-28 rounded-full mb-5 shadow-inner group-hover:scale-110 transition-transform duration-300 overflow-hidden border-4 border-white">
                <img src="https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=200&h=200&fit=crop" alt="Beto" class="w-full h-full object-cover">
              </div>
              <h3 class="text-xl font-bold text-zinc-800 font-['Poppins',_sans-serif]">Beto</h3>
              <p class="text-md text-red-500 font-medium">Desarrollador</p>
            </div>
            <div class="p-8 bg-zinc-50 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 text-center flex flex-col items-center group">
              <div class="h-28 w-28 rounded-full mb-5 shadow-inner group-hover:scale-110 transition-transform duration-300 overflow-hidden border-4 border-white">
                <img src="https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=200&h=200&fit=crop" alt="Alberto" class="w-full h-full object-cover">
              </div>
              <h3 class="text-xl font-bold text-zinc-800 font-['Poppins',_sans-serif]">Alberto</h3>
              <p class="text-md text-red-500 font-medium">Diseño UI/UX</p>
            </div>
            <div class="p-8 bg-zinc-50 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 text-center flex flex-col items-center group">
              <div class="h-28 w-28 rounded-full mb-5 shadow-inner group-hover:scale-110 transition-transform duration-300 overflow-hidden border-4 border-white">
                <img src="https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=200&h=200&fit=crop" alt="Kleber" class="w-full h-full object-cover">
              </div>
              <h3 class="text-xl font-bold text-zinc-800 font-['Poppins',_sans-serif]">Kleber</h3>
              <p class="text-md text-red-500 font-medium">Product Manager</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');
</style>
