import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Page from '../views/Page.vue'
import AddPage from '../views/AddPage.vue'
import Review from '@/components/review.vue'
import Cards from '@/components/cards.vue'
import Category from '@/components/category.vue'
import Settings from '@/components/settings.vue'
import AddCategory from '@/components/addCategory.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Page',
    component: Page,
    children: [
      { path: "", component: Review, name: "review" },
      { path: "/cards", component: Cards, name: "cards" },
      { path: "/category", component: Category, name: "category" },
      { path: "/settings", component: Settings, name: "settings" },
    ],

  },
  {
    path: "/add",
    name: "AddPage", component: AddPage,
    children: [{
      path: "category", component: AddCategory, name: "addCategory"
    }]
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
