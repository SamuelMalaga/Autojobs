import { createRouter, createWebHistory,Router } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomeView,
    meta:{requiresAuth:false}
  },
  {
    path: '/JobTracker',
    name: 'JobTracker',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/JobTracker.vue'),
    meta:{requiresAuth:true}
  },
  {
    path: '/myProfile',
    name: 'myProfile',
    component: () => import(/* webpackChunkName: "about" */ '../views/MyProfileView.vue'),
    meta:{requiresAuth:true}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token') !== null;

  if (to.matched.some(route => route.meta.requiresAuth) && !isAuthenticated) {
    // Se a rota requer autenticação e o usuário não está autenticado,
    // redirecionar para a página de login
    next('/');
  } else {
    next();
  }
});


export default router
