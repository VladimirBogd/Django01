<script setup>
import { computed, onBeforeMount, ref, watch } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";
import { storeToRefs } from "pinia";
import useUserStore from "@/stores/userStore";

const userStore = useUserStore();
const { isSuperUser, isAuthenticated, username, userId } =
  storeToRefs(userStore);

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

const selectedGuild = ref(null); // Хранит выбранную гильдию
const filteredTeams = ref([]); // Хранит команды, привязанные к выбранной гильдии

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
const customersByUserId = computed(() => {
  return _.keyBy(customers.value, (x) => x.user_id);
});

async function fetchCustomers() {
  const r = await axios.get("/api/customers/");
  customers.value = r.data;
}

async function fetchOrders() {
  loading.value = true;
  const r = await axios.get("/api/orders/");
  orders.value = r.data;
  loading.value = false;
  await fetchStats();
  await filterOrdersByUser();
}

async function onOrderAdd() {
  const formData = new FormData();
  // Получение клиента по userId
  const customerForUser = customersByUserId.value[userId.value];

  formData.set("name", orderToAdd.value.name);
  formData.set("cost", orderToAdd.value.cost);
  formData.set("guild", orderToAdd.value.guild);
  formData.set("team", orderToAdd.value.team);
  if (isSuperUser) formData.set("customer", orderToAdd.value.customer);
  else formData.set("customer", customerForUser.id);
  try {
    await axios.post("/api/orders/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    await fetchOrders();

    // Очищаем поля после успешного добавления
    orderToAdd.value.name = "";
    orderToAdd.value.cost = "";
    orderToAdd.value.guild = "";
    orderToAdd.value.team = "";
    if (isSuperUser) orderToAdd.value.customer = "";
  } catch (error) {
    console.error("Ошибка при создании заказа:", error);
  }
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
  await fetchStats();
  await filterOrdersByUser();
});

function updateTeams() {
  if (selectedGuild.value) {
    filteredTeams.value = teams.value.filter(
      (team) => team.guild === selectedGuild.value
    );
    orderToAdd.value.guild = selectedGuild.value;
  } else {
    filteredTeams.value = []; // Если гильдия не выбрана, очищаем команды
  }
}
// Устанавливаем реактивный обработчик для выбора гильдии
watch(selectedGuild, updateTeams);

const selectedUser = ref(null);
const filteredOrders = ref([]);
function filterOrdersByUser() {
  if (selectedUser.value === null) {
    filteredOrders.value = orders.value;
  } else if (selectedUser.value.user_id === userId.value && isSuperUser.value) {
    filteredOrders.value = orders.value;
  } else {
    filteredOrders.value = orders.value.filter(
      (order) => order.customer === selectedUser.value.id
    );
  }
}
// Устанавливаем реактивный обработчик для выбора гильдии
watch(selectedUser, filterOrdersByUser);

const stats = ref({});
async function fetchStats() {
  try {
    const response = await axios.get("/api/orders/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <div v-if="isAuthenticated">
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
                  required
                />
                <label for="floatingInput">Стоимость</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating mb-3">
                <select
                  class="form-select"
                  v-model="selectedGuild"
                  @change="updateTeams"
                  required
                >
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
                  v-model="orderToAdd.team"
                  :disabled="!selectedGuild"
                  required
                >
                  <option value="" disabled selected>Выберите команду</option>
                  <option :key="t.id" :value="t.id" v-for="t in filteredTeams">
                    {{ t.name }}
                  </option>
                </select>
                <label for="floatingInput">Команда</label>
              </div>
            </div>
            <div v-if="isSuperUser" class="col-auto">
              <div class="form-floating mb-3">
                <select
                  class="form-select"
                  v-model="orderToAdd.customer"
                  required
                >
                  <option :key="c.id" :value="c.id" v-for="c in customers">
                    {{ c.username }}
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

        <div class="statictics">
          <div class="stats centered-content">
            <h3 class="centered-content__title">Статистика заказов</h3>
            <p class="centered-content__item">Количество: {{ stats.count }}</p>
            <p class="centered-content__item">
              Средняя цена: {{ stats.avg.toFixed(2) }}
            </p>
            <p class="centered-content__item">
              Максимальная цена: {{ stats.max }}
            </p>
            <p class="centered-content__item">
              Минимальная цена: {{ stats.min }}
            </p>
          </div>
        </div>

        <div>
          <div v-if="isSuperUser" class="d-flex justify-content-end">
            <div class="form-floating mb-3 w-25">
              <select
                class="form-select"
                v-model="selectedUser"
                @change="filterOrdersByUser"
              >
                <option :key="c.id" :value="c" v-for="c in customers">
                  {{ c.username }}
                </option>
              </select>
              <label for="floatingInput">Фильтр по юзеру</label>
            </div>
          </div>
          <div v-for="item in filteredOrders" :key="item.id" class="order-item">
            <div>{{ item.name }}</div>
            <div>{{ item.cost }}</div>
            <div>{{ item.status }}</div>
            <div>{{ teamsById[item.team]?.name }}</div>
            <div>{{ guildsById[item.guild]?.name }}</div>
            <div>{{ customersById[item.customer]?.username }}</div>
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
                  </div>
                  <div class="col-auto">
                    <div class="form-floating mb-3">
                      <input
                        type="text"
                        class="form-control"
                        v-model="orderToEdit.cost"
                      />
                      <label for="floatingInput">Стоимость</label>
                    </div>
                  </div>

                  <div class="row">
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
                    <div class="col">
                      <div class="form-floating mb-3">
                        <select class="form-select" v-model="orderToEdit.guild">
                          <option :key="g.id" :value="g.id" v-for="g in guilds">
                            {{ g.name }}
                          </option>
                        </select>
                        <label for="floatingInput">Гильдия</label>
                      </div>
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
                  <div v-if="isSuperUser" class="col-auto">
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
                          {{ c.username }}
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
                    Закрыть
                  </button>
                  <button
                    type="button"
                    class="btn btn-primary"
                    data-bs-dismiss="modal"
                    @click="onOrderUpdate"
                  >
                    Сохранить изменения
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>Вы не авторизованы</div>
    </div>
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

.statictics {
  margin: 20px;
  padding: 20px;
  background-color: #e0f7fa; /* Более мягкий цвет фона */
  border-radius: 10px; /* Закругленные углы */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Тень */
  transition: all 0.3s ease; /* Плавный переход для эффектов при наведении */
}

.statictics:hover {
  transform: translateY(-5px); /* Поднимает блок при наведении */
}

.centered-content {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  text-align: center;
}

.centered-content__title {
  flex-basis: 100%;
  margin: 0;
  font-size: 24px; /* Увеличенный шрифт заголовка */
  font-weight: bold; /* Сделать заголовок жирным */
  color: #00796b; /* Цвет заголовка */
  margin-bottom: 15px; /* Отступ снизу */
}

.centered-content__item {
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px; /* Размер шрифта для элементов */
  color: #555; /* Цвет текста */
  border: 1px solid #00796b; /* Обводка вокруг элемента */
  border-radius: 5px; /* Закругленные углы для обводки */
  padding: 10px; /* Отступ внутри элемента для текста */
  background-color: white; /* Цвет фона для элементов */
  transition: background-color 0.3s ease; /* Плавный переход цвета фона при наведении */
}

.centered-content__item:hover {
  background-color: #f1f1f1; /* Цвет фона при наведении на элемент */
}
</style>