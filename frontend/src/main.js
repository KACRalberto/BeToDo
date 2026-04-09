import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@/tailwind/main.css'
import App from './App.vue'
import router from './router'
import 'animate.css'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

// global axios defaults for authentication
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.baseURL = "https://betodo.onrender.com"
axios.interceptors.request.use(config => {
  const token = localStorage.getItem("TOKEN")
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast, {
  transition: "Vue-Toastification__fade",
  maxToasts: 20,
  newestOnTop: true
})
app.mount('#app')
