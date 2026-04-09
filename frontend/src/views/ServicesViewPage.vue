<template>
  <div class="min-h-[83vh] w-full bg-zinc-50 py-12 px-6 flex flex-col items-center font-['Inter',_sans-serif] antialiased">
    <header class="mb-12 text-center max-w-2xl">
      <h1 class="text-4xl md:text-5xl font-extrabold text-zinc-900 mb-4 font-['Poppins',_sans-serif]">Nuestros Servicios</h1>
      <p class="text-lg text-zinc-600">Ofrecemos soluciones diseñadas para potenciar tu gestión de tareas y productividad personal al máximo.</p>
    </header>

    <section class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl mb-16">
      <article class="p-8 bg-white rounded-2xl shadow-sm border border-zinc-100 hover:shadow-md transition-shadow">
        <div class="text-3xl mb-4">✅</div>
        <h2 class="text-xl font-bold text-zinc-800 mb-3 font-['Poppins',_sans-serif]">Gestión de Tareas</h2>
        <p class="text-zinc-600 leading-relaxed">Crea, organiza y prioriza tus tareas diarias. Mantén el control de lo que debes hacer sin perder el enfoque.</p>
      </article>

      <article class="p-8 bg-white rounded-2xl shadow-sm border border-zinc-100 hover:shadow-md transition-shadow">
        <div class="text-3xl mb-4">🤝</div>
        <h2 class="text-xl font-bold text-zinc-800 mb-3 font-['Poppins',_sans-serif]">Colaboración</h2>
        <p class="text-zinc-600 leading-relaxed">Comparte tus listas, asigna tareas a otros miembros de tu equipo y colabora en tiempo real.</p>
      </article>

      <article class="p-8 bg-white rounded-2xl shadow-sm border border-zinc-100 hover:shadow-md transition-shadow">
        <div class="text-3xl mb-4">📊</div>
        <h2 class="text-xl font-bold text-zinc-800 mb-3 font-['Poppins',_sans-serif]">Estadísticas</h2>
        <p class="text-zinc-600 leading-relaxed">Visualiza tu progreso y analiza tu productividad semanal mediante gráficos intuitivos.</p>
      </article>
    </section>

    <section class="w-full max-w-5xl">
      <h3 class="text-3xl font-bold text-center text-zinc-900 mb-10 font-['Poppins',_sans-serif]">Planes Disponibles</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="p-8 bg-white border border-zinc-200 rounded-3xl flex flex-col items-center text-center hover:-translate-y-2 transition-transform duration-300 shadow-sm hover:shadow-xl">
          <h4 class="text-2xl font-bold text-zinc-800 mb-2 font-['Poppins',_sans-serif]">Básico</h4>
          <p class="text-4xl font-extrabold text-red-500 mb-4">Gratis</p>
          <p class="text-zinc-600 mb-8 flex-1">Funciones principales ideales para el uso personal y cotidiano.</p>
          <button @click="simularCompra('Básico')" class="w-full py-3 px-6 rounded-xl font-bold bg-zinc-100 text-zinc-800 hover:bg-zinc-200 transition-colors">Seleccionar</button>
        </div>
        <div class="p-8 bg-gradient-to-b from-zinc-900 to-zinc-800 border border-zinc-800 rounded-3xl flex flex-col items-center text-center hover:-translate-y-2 transition-transform duration-300 shadow-2xl relative overflow-hidden">
          <div class="absolute top-0 right-0 bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">Popular</div>
          <h4 class="text-2xl font-bold text-white mb-2 font-['Poppins',_sans-serif]">Pro</h4>
          <p class="text-4xl font-extrabold text-white mb-4">4.99€<span class="text-lg text-zinc-400 font-medium">/mes</span></p>
          <p class="text-zinc-300 mb-8 flex-1">Colaboración con equipos, recordatorios y administración avanzada.</p>
          <button @click="simularCompra('Pro')" class="w-full py-3 px-6 rounded-xl font-bold bg-red-500 text-white hover:bg-red-400 shadow-[0_4px_14px_0_rgba(239,68,68,0.39)] transition-all">Adquirir Pro</button>
        </div>
        <div class="p-8 bg-white border border-zinc-200 rounded-3xl flex flex-col items-center text-center hover:-translate-y-2 transition-transform duration-300 shadow-sm hover:shadow-xl">
          <h4 class="text-2xl font-bold text-zinc-800 mb-2 font-['Poppins',_sans-serif]">Empresa</h4>
          <p class="text-4xl font-extrabold text-red-500 mb-4">19.99€<span class="text-lg text-zinc-500 font-medium">/mes</span></p>
          <p class="text-zinc-600 mb-8 flex-1">Integraciones exclusivas y soporte prioritario 24/7 para tu empresa.</p>
          <button @click="simularCompra('Empresa')" class="w-full py-3 px-6 rounded-xl font-bold bg-zinc-100 text-zinc-800 hover:bg-zinc-200 transition-colors">Contactar Ventas</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const simularCompra = (plan) => {
  alert(`¡Procesando simulación de compra para el plan ${plan}!\n\nGracias por confiar en BeToDo.`);
}
</script>

<style scoped>
</style>
