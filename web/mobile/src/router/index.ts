import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Page from "@/views/Page.vue";
import EditorPage from "@/views/EditorPage.vue";
import CardReview from "@/views/cardReview.vue";
import SettingsContent from "@/views/SettingsContent.vue";
// 登录/注册
import LogIn from "@/views/LogIn.vue";
import SignUp from "@/views/SignUp.vue";

import Review from "@/components/review.vue";
import Cards from "@/components/cards.vue";
import Category from "@/components/category.vue";
import Settings from "@/components/settings.vue";
import AddCategory from "@/components/addCategory.vue";
import AddCard from "@/components/addCard.vue";
import EditorCategory from "@/components/EditorCategory.vue";
import EditorCard from "@/components/EditorCard.vue";
// ---- 设置内部页面
import About from "@/components/About.vue";
import Plan from "@/components/Plan.vue";
import AddPlan from "@/components/AddPlan.vue";
import EditorPlan from "@/components/EditorPlan.vue";
import Analyse from "@/components/Analyse.vue";

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
      { path: "plan", component: AddPlan, name: "addPlan" },
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
      { path: "plan/:pid", component: EditorPlan, name: "editorPlan" },
    ],
  },
  {
    path: "/review/review-mode",
    name: "CardReview",
    component: CardReview,
  },
  {
    path: "/settings",
    component: SettingsContent,
    children: [
      {
        path: "about",
        component: About,
        name: "About",
      },
      { path: "plans", component: Plan, name: "Plan" },
      { path: "analyse", component: Analyse, name: "Analyse" },
    ],
  },
  {
    path: "/login",
    component: LogIn,
    name: "LogIn"
  },
  {
    path: "/signup",
    component: SignUp,
    name: "SignUp"
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
