import Matches from "@/views/dashboard/matches/Matches";

const MatchesRoutes = {
  component: () => import("../Index.vue"),
  children: [
    {
      name: "Matches",
      path: "/matches",
      component: Matches,
      meta: {
        title: "Matches",
      },
    },
  ],
};

export default MatchesRoutes;
