import { createRouter, createWebHistory } from 'vue-router'
import { useToast } from "vue-toastification";



const toast = useToast()

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{ path: '/', component: () => import('@/views/homeViewPage.vue'), meta:{isPublic: true} },
    {path: "/register", component: ()=> import("@/views/RegisterViewPage.vue")},
    {path: "/login", component: ()=> import("@/views/LoginViewPage.vue")},
    {path: "/forgot-password", component: ()=> import("@/views/ForgotPasswordViewPage.vue"), meta:{isPublic: true}},
    {path: "/reset-password", component: ()=> import("@/views/ResetPasswordViewPage.vue"), meta:{isPublic: true}},
    {path: "/services", component: ()=> import("@/views/ServicesViewPage.vue"), meta:{isPublic: true}},
    {path: "/about", component: ()=> import("@/views/AboutViewPage.vue"), meta:{isPublic: true}},
    {path: "/contact", component: ()=> import("@/views/ContactViewPage.vue"), meta:{isPublic: true}},
    {path : "/home", component: ()=> import("@/views/homeUserViewPage.vue"), meta:{requiresToken : true}},
    // catch-all 404 route (must be last)
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFoundView.vue'), meta: { isPublic: true } }

  ],
})

router.beforeEach((to,from,next)=>{
  const token = localStorage.getItem("TOKEN")
  
  // Si intentas ir a login o register y ya tienes token, redirige a /home
  if((to.path === "/login" || to.path === "/register") && token){
    next("/home")
    return
  }
  
  // Si ir a "/" y tienes token, redirige a /home
  if(to.path === "/" && token){
    next("/home")
    return
  }
  
  // Si intentas ir a una ruta protegida sin token, redirige a login
  if(to.meta.requiresToken && !token){
    toast.error("Debes iniciar sesión")
    next("/login")
  }else{
    next()
  }
})


export default router
