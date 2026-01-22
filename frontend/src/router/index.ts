import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Page",
    component: () => import("@/views/Page.vue"),
    children: [
      {
        path: "",
        component: () => import("@/components/review.vue"),
        name: "review",
      },
      {
        path: "/cards",
        component: () => import("@/components/cards.vue"),
        name: "cards",
      },
      {
        path: "/category",
        component: () => import("@/components/category.vue"),
        name: "category",
      },
      {
        path: "/settings",
        component: () => import("@/components/settings.vue"),
        name: "settings",
      },
    ],
  },
  {
    path: "/add",
    name: "AddPage",
    component: () => import("@/views/EditorPage.vue"),
    children: [
      {
        path: "category",
        component: () => import("@/components/addCategory.vue"),
        name: "addCategory",
      },
      {
        path: "card",
        component: () => import("@/components/addCard.vue"),
        name: "addCard",
      },
      {
        path: "plan",
        component: () => import("@/components/AddPlan.vue"),
        name: "addPlan",
      },
    ],
  },
  {
    path: "/editor",
    name: "EditorPage",
    component: () => import("@/views/EditorPage.vue"),
    children: [
      {
        path: "category/:cid",
        component: () => import("@/components/EditorCategory.vue"),
        name: "editorCategory",
      },
      {
        path: "card/:cid",
        component: () => import("@/components/EditorCard.vue"),
        name: "editorCard",
      },
      {
        path: "plan/:pid",
        component: () => import("@/components/EditorPlan.vue"),
        name: "editorPlan",
      },
    ],
  },
  {
    path: "/review/review-mode",
    name: "CardReview",
    component: () => import("@/views/cardReview.vue"),
  },
  {
    path: "/settings",
    component: () => import("@/views/SettingsContent.vue"),
    children: [
      {
        path: "plans",
        component: () => import("@/components/Plan.vue"),
        name: "Plan",
      },
      {
        path: "analyse",
        component: () => import("@/components/Analyse.vue"),
        name: "Analyse",
      },
      {
        path: "profile",
        component: () => import("@/components/Profile.vue"),
        name: "Profile",
      },
      {
        path: "help",
        component: () => import("@/components/Help.vue"),
        name: "Help",
      },
    ],
  },
  // 数据分析
  {
    path: "/analyse",
    component: () => import("@/views/SettingsContent.vue"),
    children: [
      {
        path: "review",
        component: () => import("@/components/AnalyseReview.vue"),
        name: "analyseReview",
      },
      {
        path: "create",
        component: () => import("@/components/AnalyseCreate.vue"),
        name: "analyseCreate",
      },
    ],
  },
  {
    path: "/login",
    component: () => import("@/views/LogIn.vue"),
    name: "LogIn",
  },
  {
    path: "/signup",
    component: () => import("@/views/SignUp.vue"),
    name: "SignUp",
  },
  {
    path: "/404",
    name: "404",
    meta: {
      title: "无法访问",
    },
    component: () => import("@/views/NotFound.vue"),
  },
  {
    path: "/:pathMatch(.*)",
    redirect: "/404",
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
