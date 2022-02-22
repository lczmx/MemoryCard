import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Page from "@/views/Page.vue";
import EditorPage from "@/views/EditorPage.vue";
import CardReview from "@/views/cardReview.vue";

import Review from "@/components/review.vue";
import Cards from "@/components/cards.vue";
import Category from "@/components/category.vue";
import Settings from "@/components/settings.vue";
import AddCategory from "@/components/addCategory.vue";
import AddCard from "@/components/addCard.vue";
import EditorCategory from "@/components/EditorCategory.vue";
import EditorCard from "@/components/EditorCard.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Page",
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
    name: "AddPage",
    component: EditorPage,
    children: [
      { path: "category", component: AddCategory, name: "addCategory" },
      { path: "card", component: AddCard, name: "addCard" },
    ],
  },
  {
    path: "/editor",
    name: "EditorPage",
    component: EditorPage,
    children: [
      {
        path: "category/:cid",
        component: EditorCategory,
        name: "editorCategory",
      },
      { path: "card/:cid", component: EditorCard, name: "editorCard" },
    ],
  },
  {
    path: "/review/review-mode",
    name: "CardReview",
    component: CardReview,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
