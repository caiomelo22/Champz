import Draft from "@/views/dashboard/draft/Draft";

const DraftRoutes = {
  component: () => import("../Index.vue"),
  children: [
    {
      name: "Draft",
      path: "/draft",
      component: Draft,
      meta: {
        title: "Draft",
      },
    },
  ],
};

export default DraftRoutes;
