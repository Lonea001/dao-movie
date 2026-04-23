import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        { path: '',             name: 'Home',           component: () => import('@/views/Home.vue') },
        { path: 'movies',       name: 'MovieList',      component: () => import('@/views/MovieList.vue') },
        { path: 'movies/:id',   name: 'MovieDetail',    component: () => import('@/views/MovieDetail.vue') },
        { path: 'rankings',     name: 'Rankings',       component: () => import('@/views/Rankings.vue') },
        { path: 'rankings/:id', name: 'RankingDetail',  component: () => import('@/views/RankingDetail.vue') },
      ]
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      children: [
        { path: '',     name: 'AdminLogin',   component: () => import('@/views/admin/Login.vue') },
        { path: 'home', 
          name: 'AdminHome',    
          component: () => import('@/views/admin/AdminHome.vue'),
          meta: { requiresAuth: true }
        },
      ]
    }

  ],

  // 跳转新页面时，回到顶部 
  scrollBehavior: () => ({ top: 0 })
})

// 管理员守卫
router.beforeEach( (to) => {
  if (to.meta.requiresAuth){
    const token = localStorage.getItem('admin_token')
    if (!token) return { path: '/admin'}
  }
})

export default router