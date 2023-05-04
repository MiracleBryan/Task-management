
const routes = [
  {
    path: '/',
    redirect: { path: '/tasks' }
  },

  {
    path: '/tasks',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/task/TaskPage.vue') },
      { path: '/tasks?user=:id', component: () => import('pages/task/TaskPage.vue') },
    ],
    meta: {
      requiresAuth: true
    }
  },

  {
    path: '/login',
    name: 'login',
    component: () => import('pages/authentication/LoginPage.vue')
  },

  {
    path: '/signup',
    name: 'register',
    component: () => import('pages/authentication/RegisterPage.vue')
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
