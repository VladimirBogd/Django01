import CustomersView from '@/views/CustomersView.vue'
import GuildsView from '@/views/GuildsView.vue'
import OrdersView from '@/views/OrdersView.vue'
import WizardsView from '@/views/WizardsView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "WizardsView",
      component: WizardsView,
    },
    {
      path: "/guilds",
      name: "GuildsView",
      component: GuildsView,
    },
    {
      path: "/customers",
      name: "CustomersView",
      component: CustomersView,
    },
    {
      path: "/orders",
      name: "OrdersView",
      component: OrdersView,
    },
  ]
})

export default router
