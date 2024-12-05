<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

import { useRouter } from "vue-router";
import useUserStore from "@/stores/userStore";

const userStore = useUserStore();
// Проверка, вошел ли пользователь в систему
const isLoggedIn = computed(() => {
  return userStore.isAuthenticated; // Используем isAuthenticated из userStore
});

onBeforeMount(() => {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);

const orders = ref([]);
const orderStatuses = ref([]);
const teams = ref([]);
const guilds = ref([]);
const customers = ref([]);
const orderToAdd = ref({});
const orderToEdit = ref({});

async function fetchOrderStatuses() {
  const r = await axios.get("/api/order-statuses/");
  orderStatuses.value = r.data;
}

const teamsById = computed(() => {
  return _.keyBy(teams.value, (x) => x.id);
});

async function fetchTeams() {
  const r = await axios.get("/api/teams/");
  teams.value = r.data;
}

const guildsById = computed(() => {
  return _.keyBy(guilds.value, (x) => x.id);
});

async function fetchGuilds() {
  const r = await axios.get("/api/guilds/");
  guilds.value = r.data;
}

const customersById = computed(() => {
  return _.keyBy(customers.value, (x) => x.id);
});

async function fetchCustomers() {
  const r = await axios.get("/api/customers/");
  customers.value = r.data;
}

async function fetchOrders() {
  loading.value = true;
  const r = await axios.get("/api/orders/");
  console.log(r.data);
  orders.value = r.data;
  loading.value = false;
}

async function onOrderAdd() {
  await axios.post("/api/orders/", {
    ...orderToAdd.value,
  });
  await fetchOrders(); // переподтягиваю
}

async function OnOrderEdit(order) {
  orderToEdit.value = { ...order };
}

async function onOrderUpdate() {
  await axios.put(`/api/orders/${orderToEdit.value.id}/`, {
    ...orderToEdit.value,
  });
  await fetchOrders();
}

async function OnOrderRemove(order) {
  await axios.delete(`/api/orders/${order.id}/`);
  await fetchOrders();
}

onBeforeMount(async () => {
  await fetchOrders();
  await fetchTeams();
  await fetchGuilds();
  await fetchCustomers();
  await fetchOrderStatuses();
});
</script>

<template>
  <div class="container-fluid">
    <form v-if="isLoggedIn">
      <div class="p-2">
        <form @submit.prevent.stop="onOrderAdd">
          <div class="row">
            <div class="col">
              <div class="form-floating mb-3">
                <input
                  type="text"
                  class="form-control"
                  v-model="orderToAdd.name"
                  required
                />
                <label for="floatingInput">Название</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating mb-3">
                <input
                  type="text"
                  class="form-control"
                  v-model="orderToAdd.cost"
                />
                <label for="floatingInput">Стоимость</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating mb-3">
                <select
                  class="form-select"
                  v-model="orderToAdd.status"
                  required
                >
                  <option :key="s.id" :value="s.id" v-for="s in orderStatuses">
                    {{ s.name }}
                  </option>
                </select>
                <label for="floatingInput">Статус</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating mb-3">
                <select class="form-select" v-model="orderToAdd.guild" required>
                  <option :key="g.id" :value="g.id" v-for="g in guilds">
                    {{ g.name }}
                  </option>
                </select>
                <label for="floatingInput">Гильдия</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating mb-3">
                <select class="form-select" v-model="orderToAdd.team" required>
                  <option :key="t.id" :value="t.id" v-for="t in teams">
                    {{ t.name }}
                  </option>
                </select>
                <label for="floatingInput">Команда</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating mb-3">
                <select
                  class="form-select"
                  v-model="orderToAdd.customer"
                  required
                >
                  <option :key="c.id" :value="c.id" v-for="c in customers">
                    {{ c.name }}
                  </option>
                </select>
                <label for="floatingInput">Заказчик</label>
              </div>
            </div>
            <div class="col-auto">
              <button class="btn btn-primary">Добавить</button>
            </div>
          </div>
        </form>

        <div v-if="loading">Гружу...</div>

        <div>
          <div v-for="item in orders" :key="item.id" class="order-item">
            <div>{{ item.name }}</div>
            <div>{{ item.cost }}</div>
            <div>{{ item.status }}</div>
            <div>{{ teamsById[item.team]?.name }}</div>
            <div>{{ guildsById[item.guild]?.name }}</div>
            <div>{{ customersById[item.customer]?.name }}</div>
            <button
              class="btn btn-success"
              @click="OnOrderEdit(item)"
              data-bs-toggle="modal"
              data-bs-target="#editOrderModal"
            >
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-danger" @click="OnOrderRemove(item)">
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>

        <div
          class="modal fade"
          id="editOrderModal"
          tabindex="-1"
          aria-labelledby="editOrderModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="editOrderModalLabel">
                  Редактировать
                </h1>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <div class="row">
                  <div class="col">
                    <div class="form-floating mb-3">
                      <input
                        type="text"
                        class="form-control"
                        v-model="orderToEdit.name"
                      />
                      <label for="floatingInput">Название</label>
                    </div>
                    <div class="col">
                      <div class="form-floating mb-3">
                        <input
                          type="text"
                          class="form-control"
                          v-model="orderToEdit.cost"
                        />
                        <label for="floatingInput">Стоимость</label>
                      </div>
                    </div>
                  </div>
                  <div class="col-auto">
                    <div class="form-floating mb-3">
                      <select
                        class="form-select"
                        v-model="orderToEdit.status"
                        required
                      >
                        <option
                          :key="s.id"
                          :value="s.id"
                          v-for="s in orderStatuses"
                        >
                          {{ s.name }}
                        </option>
                      </select>
                      <label for="floatingInput">Статус</label>
                    </div>
                  </div>
                  <div class="col-auto">
                    <div class="form-floating mb-3">
                      <select class="form-select" v-model="orderToEdit.guild">
                        <option :key="g.id" :value="g.id" v-for="g in guilds">
                          {{ g.name }}
                        </option>
                      </select>
                      <label for="floatingInput">Гильдия</label>
                    </div>
                  </div>
                  <div class="col-auto">
                    <div class="form-floating mb-3">
                      <select
                        class="form-select"
                        v-model="orderToEdit.team"
                        required
                      >
                        <option :key="t.id" :value="t.id" v-for="t in teams">
                          {{ t.name }}
                        </option>
                      </select>
                      <label for="floatingInput">Команда</label>
                    </div>
                  </div>
                  <div class="col-auto">
                    <div class="form-floating mb-3">
                      <select
                        class="form-select"
                        v-model="orderToEdit.customer"
                        required
                      >
                        <option
                          :key="c.id"
                          :value="c.id"
                          v-for="c in customers"
                        >
                          {{ c.name }}
                        </option>
                      </select>
                      <label for="floatingInput">Заказчик</label>
                    </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button
                    type="button"
                    class="btn btn-primary"
                    data-bs-dismiss="modal"
                    @click="onOrderUpdate"
                  >
                    Save changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
    <form form v-else class="container-fluid">Вы не авторизованы</form>
  </div>
</template>

<style lang="scss" scoped>
.order-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto auto auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}
</style>