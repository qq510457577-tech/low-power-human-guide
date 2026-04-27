import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/self-test',
    name: 'SelfTest',
    component: () => import('@/views/SelfTest.vue'),
  },
  {
    path: '/daily-actions',
    name: 'DailyActions',
    component: () => import('@/views/DailyActions.vue'),
  },
  {
    path: '/articles',
    name: 'Articles',
    component: () => import('@/views/Articles.vue'),
  },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: () => import('@/views/ArticleDetail.vue'),
    props: true,
  },
  {
    path: '/share/submit',
    name: 'ShareSubmit',
    component: () => import('@/views/ShareSubmit.vue'),
  },
  {
    path: '/share/square',
    name: 'ShareSquare',
    component: () => import('@/views/ShareSquare.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
