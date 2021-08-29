import Vue from "vue";
import Router from "vue-router";
import Draft from "./views/dashboard/draft/routes";
import Index from "./views/dashboard/Index";
import Matches from "./views/dashboard/matches/routes";

Vue.use(Router);

const router = new Router({
  base: "http://localhost:8080/",
  linkActiveClass: "active",
  linkExactActiveClass: "exact-active",
  component: () => Index,
  mode: "history",
  routes: [
    {
      path: "/draft",
      ...Draft,
    },
    {
      path: "/matches",
      ...Matches,
    },
  ],
});

export default router;