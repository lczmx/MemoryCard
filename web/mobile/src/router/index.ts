import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Page from '../views/Page.vue'
import Review from '@/components/review.vue'
import Cards from '@/components/cards.vue'
import Tags from '@/components/tags.vue'
import Settings from '@/components/settings.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Page',
    component: Page,
    children: [
      { path: "", component: Review, },
      { path: "/cards", component: Cards, },
      { path: "/tags", component: Tags, },
      { path: "/settings", component: Settings, },
    ],

  },

  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
