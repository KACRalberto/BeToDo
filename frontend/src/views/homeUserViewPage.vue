<template>
  <!-- CONTENEDOR PRINCIPAL: h-screen y overflow-hidden SOLO en PC (lg:). En móvil permite scroll normal -->
  <div class="min-h-screen lg:h-screen w-full bg-zinc-950 text-zinc-200 flex flex-col font-['Inter',_sans-serif] antialiased lg:overflow-hidden">
    
    <!-- HEADER (Fijo arriba sin encogerse) -->
    <header class="bg-zinc-900 border-b border-zinc-800 py-3 px-6 flex justify-between items-center shadow-md flex-shrink-0 z-10">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-red-500 to-orange-500 rounded-xl shadow-md flex items-center justify-center">
          <span class="text-white font-bold text-xl">B</span>
        </div>
        <h1 class="text-xl lg:text-2xl font-extrabold tracking-tight text-white flex items-center font-['Poppins',_sans-serif]">
          BeToDo
          <span class="text-zinc-500 font-medium text-base ml-3 hidden sm:inline-block">| {{ user }}</span>
        </h1>
      </div>
      
      <button @click="cerrar" class="text-sm bg-zinc-800 hover:bg-red-600 text-zinc-300 hover:text-white px-4 py-2 rounded-lg font-semibold transition-all duration-300 shadow-sm outline-none">
        Cerrar Sesión
      </button>
    </header>

    <!-- ZONA CENTRAL: Bloqueada en PC, expandible en móvil -->
    <main class="w-full lg:max-w-[1700px] mx-auto flex flex-col lg:flex-row p-4 lg:p-6 gap-6 lg:min-h-0 lg:overflow-hidden bg-zinc-950">
      
      <!-- PANEL IZQUIERDO (TAREAS) -->
      <section class="flex flex-col lg:flex-1 bg-zinc-900 border border-zinc-800 rounded-3xl shadow-lg overflow-hidden min-h-[50vh] lg:min-h-0">
        
        <!-- Cabecera de Tareas (Fija dentro del panel) -->
        <div class="flex flex-wrap gap-4 justify-between items-end p-5 lg:p-6 border-b border-zinc-800 flex-shrink-0 bg-zinc-900 z-10">
          <div>
            <h2 class="text-xl lg:text-2xl font-bold text-white tracking-tight font-['Poppins',_sans-serif]">Mis Tareas</h2>
            <p class="text-zinc-500 text-sm mt-1">Gestiona tus actividades pendientes</p>
          </div>
          <button v-if="tareas.length > 0" @click="eliminarTodasLasTareas" class="text-xs lg:text-sm bg-red-500/10 hover:bg-red-500/20 text-red-500 px-3 py-1.5 rounded-lg font-medium transition-colors">
            Limpiar Todo
          </button>
        </div>

        <!-- Lista de Tareas (AQUÍ ESTÁ EL ÚNICO SCROLL PERMITIDO) -->
        <div class="flex-1 overflow-y-auto p-5 lg:p-6 custom-scrollbar min-h-0 bg-zinc-900/50">
          <div v-if="tareas.length === 0" class="flex flex-col items-center justify-center text-center h-full opacity-60">
            <div class="w-16 h-16 mb-4 rounded-full bg-zinc-800 flex items-center justify-center">
              <span class="text-3xl">☕</span>
            </div>
            <h3 class="text-lg font-medium text-white font-['Poppins',_sans-serif]">Todo al día</h3>
            <p class="text-sm text-zinc-400 mt-2">No tienes tareas pendientes, ¡disfruta tu tiempo!</p>
          </div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4 content-start">
            <div v-for="tarea in tareas" :key="tarea.id" class="group relative bg-zinc-800/80 border rounded-2xl p-4 hover:shadow-lg transition-all duration-300 flex flex-col gap-3 h-full" :class="tarea.estado === 'completada' ? 'border-green-500/30 bg-green-950/20 opacity-75' : 'border-zinc-700/50 hover:border-zinc-600'">
              <!-- INFO TAREA -->
              <div class="flex flex-col gap-2 flex-1">
                <div class="flex items-start justify-between gap-2">
                  <h3 class="font-bold text-base lg:text-lg leading-tight break-words font-['Poppins',_sans-serif]" :class="tarea.estado === 'completada' ? 'text-green-400 line-through' : 'text-zinc-100'">
                    {{ tarea.titulo }}
                  </h3>
                  <span class="text-[10px] uppercase tracking-wider font-bold px-2 py-1 rounded-md flex-shrink-0" :class="{ 'bg-yellow-500/10 text-yellow-500': tarea.estado === 'pendiente', 'bg-blue-500/10 text-blue-400': tarea.estado === 'en_marcha', 'bg-green-500/10 text-green-400': tarea.estado === 'completada' }">
                    {{ tarea.estado === 'en_marcha' ? 'En marcha' : tarea.estado === 'completada' ? 'Completada' : 'Pendiente' }}
                  </span>
                </div>
                <p class="text-xs lg:text-sm text-zinc-400 leading-relaxed line-clamp-3">{{ tarea.descripcion }}</p>
              </div>

              <!-- BOTONES -->
              <div class="flex flex-wrap gap-2 pt-3 border-t border-zinc-700/50 mt-auto">
                <button v-if="tarea.estado !== 'completada'" @click="marcarComoCompletada(tarea)" class="flex-1 flex justify-center items-center gap-1.5 bg-green-500/10 hover:bg-green-500/20 text-green-400 py-1.5 px-2 rounded-lg font-medium transition text-xs">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                  Completar
                </button>
                <button @click="editarTarea(tarea)" class="flex-1 flex justify-center items-center gap-1.5 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 py-1.5 px-2 rounded-lg font-medium transition text-xs">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                  Editar
                </button>
                <button @click="eliminarTarea(tarea.id, tarea.titulo)" class="flex-1 flex justify-center items-center gap-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 py-1.5 px-2 rounded-lg font-medium transition text-xs">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  Eliminar
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- PANEL DERECHO (FORMULARIOS) -->
      <aside class="w-full lg:w-[340px] xl:w-[380px] flex flex-col gap-6 flex-none lg:overflow-hidden lg:min-h-0 pb-6 lg:pb-0">
        
        <!-- PANEL: CREAR TAREA -->
        <form @submit.prevent="postTareas" class="bg-zinc-900 border border-zinc-800 rounded-3xl shadow-lg p-5 relative overflow-hidden flex-shrink-0">
          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-500 to-orange-500"></div>
          <h3 class="text-lg font-bold text-white mb-3 font-['Poppins',_sans-serif]">Añadir Tarea</h3>
          
          <div class="space-y-3">
            <div>
              <label class="block text-xs font-medium text-zinc-400 mb-1">Título</label>
              <input type="text" v-model="tarea" class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-red-500/50 text-zinc-100 transition-all placeholder-zinc-600" placeholder="¿Qué necesitas hacer?" required />
            </div>
            <div>
              <label class="block text-xs font-medium text-zinc-400 mb-1">Descripción</label>
              <input type="text" v-model="descripcionTarea" class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-red-500/50 text-zinc-100 transition-all placeholder-zinc-600" placeholder="Detalles opcionales..." />
            </div>
            <div>
              <label class="block text-xs font-medium text-zinc-400 mb-1">Estado</label>
              <select v-model="estadoTarea" class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-red-500/50 text-zinc-100 transition-all appearance-none cursor-pointer">
                <option value="pendiente">⏳ Pendiente</option>
                <option value="en_marcha">🏃 En marcha</option>
                <option value="completada">✅ Completada</option>
              </select>
            </div>
            <button type="submit" class="w-full bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 text-white text-sm font-bold py-2 rounded-xl shadow-md shadow-red-500/20 transition-all mt-1">
              Guardar Tarea
            </button>
          </div>
        </form>

        <!-- PANEL: POMODORO -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-3xl shadow-lg p-5 relative overflow-hidden flex-shrink-0">
          <div class="absolute top-0 left-0 w-full h-1" :class="enDescanso ? 'bg-gradient-to-r from-blue-500 to-cyan-500' : 'bg-gradient-to-r from-red-500 to-orange-500'"></div>
          <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2 font-['Poppins',_sans-serif]">
            <span class="text-xl">🍅</span> Pomodoro
          </h3>

          <div class="space-y-3">
            <div>
              <label class="block text-xs font-medium text-zinc-400 mb-1">Enfócate en:</label>
              <select v-model="tareaPomodoro" class="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-red-500/50 text-zinc-100 transition-all appearance-none cursor-pointer">
                <option value="">-- Selecciona una tarea --</option>
                <option v-for="t in tareas.filter((t) => t.estado !== 'completada')" :key="t.id" :value="t.id">
                  {{ t.titulo }}
                </option>
              </select>
            </div>

            <!-- Display Temporizador -->
            <div class="bg-zinc-950 border border-zinc-800/80 rounded-2xl p-4 text-center shadow-inner relative overflow-hidden">
              <div class="absolute inset-0 bg-red-500/5 blur-2xl rounded-full" v-if="pomodoroActivo && !enDescanso"></div>
              <div class="text-4xl lg:text-5xl font-black font-mono tracking-wider relative z-10" :class="enDescanso ? 'text-blue-400' : (pomodoroActivo ? 'text-red-500' : 'text-zinc-100')">
                {{ formatoTiempo(tiempoRestante) }}
              </div>
              <p class="text-xs font-medium mt-1 uppercase tracking-widest relative z-10" :class="enDescanso ? 'text-blue-500' : 'text-zinc-500'">
                {{ enDescanso ? '☕ Descanso' : pomodoroActivo ? '⏱️ En progreso' : 'Listo para iniciar' }}
              </p>
            </div>

            <!-- Botones Pomodoro -->
            <div class="flex flex-col gap-2">
              <button v-if="!pomodoroActivo && !enDescanso" @click="iniciarPomodoro" :disabled="!tareaPomodoro" class="w-full bg-zinc-100 hover:bg-white text-zinc-900 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-bold py-2 rounded-xl transition-all shadow-sm">
                ▶ Iniciar Sesión
              </button>
              
              <button v-else-if="pomodoroActivo && !enDescanso" @click="pausarPomodoro" class="w-full bg-yellow-500/10 hover:bg-yellow-500/20 text-yellow-500 text-sm font-bold py-2 rounded-xl transition-all border border-yellow-500/20">
                ⏸ Pausar
              </button>

              <button v-if="pomodoroActivo && !enDescanso" @click="iniciarDescanso" class="w-full bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 text-sm font-bold py-2 rounded-xl transition-all border border-blue-500/20">
                ☕ Tomar Descanso
              </button>

              <button v-if="enDescanso" @click="terminarDescanso" class="w-full bg-blue-500 hover:bg-blue-400 text-white text-sm font-bold py-2 rounded-xl transition-all shadow-md shadow-blue-500/20">
                Volver al Trabajo
              </button>

              <button v-if="tareaPomodoro && !enDescanso" @click="completarTareaPomodoro" class="w-full bg-green-500/10 hover:bg-green-500/20 text-green-400 text-sm font-bold py-2 rounded-xl transition-all border border-green-500/20">
                ✓ Marcar como Completada
              </button>
            </div>
          </div>
        </div>
      </aside>
    </main>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const user = ref('')
const tarea = ref('')
const descripcionTarea = ref('')
const estadoTarea = ref('pendiente')
const tareas = ref([])
const router = useRouter()

/* Estilos personalizados para la barra de desplazamiento */
const style = document.createElement('style');
style.textContent = `
  .custom-scrollbar::-webkit-scrollbar { width: 6px; }
  .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
  .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #3f3f46; border-radius: 20px; }
  .custom-scrollbar::-webkit-scrollbar-thumb:hover { background-color: #52525b; }
`;
document.head.appendChild(style);

// POMODORO
const tareaPomodoro = ref('')
const pomodoroActivo = ref(false)
const enDescanso = ref(false)
const tiempoRestante = ref(1500)
const tiempoDescanso = 300
const intervaloPomodoro = ref(null)

// --- ESTO ES CLAVE PARA JWT ---
// JWT se maneja globalmente en main.js con interceptor

watch(tareaPomodoro, (newValue) => {
  if (newValue) {
    pausarPomodoro()
    enDescanso.value = false
    tiempoRestante.value = 1500
  }
})

const formatoTiempo = (segundos) => {
  const minutos = Math.floor(segundos / 60)
  const secs = segundos % 60
  return `${String(minutos).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

const iniciarPomodoro = () => {
  if (!tareaPomodoro.value) return
  pomodoroActivo.value = true
  intervaloPomodoro.value = setInterval(() => {
    tiempoRestante.value--
    if (tiempoRestante.value <= 0) pausarPomodoro()
  }, 1000)
}

const pausarPomodoro = () => {
  pomodoroActivo.value = false
  if (intervaloPomodoro.value) clearInterval(intervaloPomodoro.value)
}

const iniciarDescanso = () => {
  pausarPomodoro()
  enDescanso.value = true
  tiempoRestante.value = tiempoDescanso
  intervaloPomodoro.value = setInterval(() => {
    tiempoRestante.value--
    if (tiempoRestante.value <= 0) terminarDescansoAutomatico()
  }, 1000)
}

const terminarDescanso = () => {
  if (intervaloPomodoro.value) clearInterval(intervaloPomodoro.value)
  enDescanso.value = false
  tiempoRestante.value = 1500
}

const terminarDescansoAutomatico = () => {
  if (intervaloPomodoro.value) clearInterval(intervaloPomodoro.value)
  enDescanso.value = false
  tiempoRestante.value = 1500
  pausarPomodoro()
  alert('¡Descanso terminado! Tiempo de volver al trabajo 💪')
}

const completarTareaPomodoro = async () => {
  try {
    if (!tareaPomodoro.value) return
    const res = await axios.put(
      `tareas/${tareaPomodoro.value}`,
      {
        estado: 'completada',
      },
    ) // JWT manejado por interceptor global

    pausarPomodoro()
    tareaPomodoro.value = ''
    tiempoRestante.value = 1500
    enDescanso.value = false
    await getTareas()
  } catch (error) {
    console.error('Error:', error)
    if (error.response?.status === 401) cerrar()
  }
}

const marcarComoCompletada = async (tarea) => {
  try {
    await axios.put(
      `tareas/${tarea.id}`,
      {
        estado: 'completada',
      },
    )
    await getTareas()
  } catch (error) {
    alert('No se pudo actualizar la tarea')
    if (error.response?.status === 401) cerrar()
  }
}

const editarTarea = async (tarea) => {
  const nuevoTitulo = prompt('Nuevo título:', tarea.titulo)
  if (nuevoTitulo === null) return
  const nuevaDesc = prompt('Nueva descripción:', tarea.descripcion)
  if (nuevaDesc === null) return
  let nuevoEstado = prompt('Nuevo estado (pendiente/en_marcha/completada):', tarea.estado)
  if (nuevoEstado === null) return
  nuevoEstado = nuevoEstado.trim().toLowerCase()
  if (!['pendiente', 'en_marcha', 'completada'].includes(nuevoEstado))
    return alert('Estado inválido [debe ser alguno de los siguientes: pendiente/en_marcha/completada]')

  try {
    await axios.put(
      `tareas/${tarea.id}`,
      {
        titulo: nuevoTitulo,
        descripcion: nuevaDesc,
        estado: nuevoEstado,
      },
    )
    await getTareas()
  } catch (error) {
    alert('No se pudo actualizar la tarea')
    if (error.response?.status === 401) cerrar()
  }
}

const eliminarTarea = async (tareaId, nombreTarea) => {
  if (!confirm(`¿Estás seguro de querer eliminar la tarea "${nombreTarea}"?`)) return
  try {
    await axios.delete(`tareas/${tareaId}`)
    await getTareas()
  } catch (error) {
    alert('Error al eliminar la tarea')
    if (error.response?.status === 401) cerrar()
  }
}

const eliminarTodasLasTareas = async () => {
  if (!confirm(`¿Estás seguro de querer eliminar TODAS las tareas?`)) return
  try {
    await axios.delete(`tareas`)
    await getTareas()
  } catch (error) {
    alert('Error al eliminar las tareas')
    if (error.response?.status === 401) cerrar()
  }
}

onMounted(() => {
  return () => {
    if (intervaloPomodoro.value) clearInterval(intervaloPomodoro.value)
  }
})

const cerrar = () => {
  // Ya no hacemos la petición axios al backend porque no hay ruta /logout
  localStorage.removeItem('TOKEN')
  localStorage.removeItem('USER_ID')
  router.push('/login')
}

const getTareas = async () => {
  try {
    const res = await axios.get('tareas')
    if (res.data.ok) tareas.value = res.data.tareas
  } catch (error) {
    if (error.response?.status === 401) cerrar()
  }
}

const postTareas = async () => {
  try {
    const clean = (str) => str.replace(/<[^>]*>?/gm, '')
    await axios.post(
      'tareas',
      {
        titulo: clean(tarea.value),
        descripcion: clean(descripcionTarea.value),
        estado: estadoTarea.value,
      },
    )

    tarea.value = ''
    descripcionTarea.value = ''
    estadoTarea.value = 'pendiente'
    await getTareas()
  } catch (error) {
    if (error.response?.status === 401) cerrar()
  }
}

onMounted(async () => {
  const token = localStorage.getItem('TOKEN')
  if (!token) {
    router.push('/login')
    return
  }
  const storedUser = localStorage.getItem('USER_ID')
  if (storedUser) {
    try {
      const userData = JSON.parse(storedUser)
      user.value = userData.email || userData
    } catch {
      user.value = storedUser
    }
  }
  await getTareas()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');
</style>
