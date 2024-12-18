<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useRouter } from "vue-router";
import useUserStore from "@/stores/userStore";
import axios from "axios";

const users = ref([]);

const username = ref("");
const pass = ref("");

const userStore = useUserStore();
const router = useRouter();

// Проверка, вошел ли пользователь в систему
const isLoggedIn = computed(() => {
  return userStore.isAuthenticated; // Используем isAuthenticated из userStore
});
const isSuperUser = computed(() => {
  return userStore.isSuperUser;
});

// Метод для получения пользователей
async function fetchUsers() {
  try {
    const response = await axios.get("/api/users/"); // Корректный путь к API
    users.value = response.data; // Сохраняем полученные данные в состоянии
  } catch (error) {
    console.error("Ошибка при получении пользователей:", error);
  }
}

async function login() {
  let token = $cookies.get("csrftoken");
  console.log(token);

  try {
    const response = await axios.post(
      "/api/users/login/",
      {
        user: username.value,
        pass: pass.value,
      },
      {
        headers: {
          "X-CSRFToken": token,
        },
      }
    );
    await userStore.fetchUser();
    await fetchUsers();
    router.push("/");
  } catch (error) {
    console.error("Ошибка при входе:", error);
  }
}

async function logout() {
  try {
    await axios.get("/api/users/logout/");
    await userStore.fetchUser();
    users.value = [];
    router.push("/");
  } catch (error) {
    console.error("Ошибка при выходе:", error);
  }
}

onBeforeMount(async () => {
  if (isSuperUser) {
    await fetchUsers();
  }
});
</script>

<template>
  <div class="container mt-5">
    <h1 class="text-center">Авторизация</h1>
    <div v-if="!isLoggedIn">
      <form @submit.prevent="login" class="w-50 mx-auto">
        <div class="mb-3">
          <label for="username" class="form-label">Имя пользователя:</label>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="username"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Пароль:</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="pass"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">Войти</button>
      </form>
    </div>

    <div v-else>
      <form @submit.prevent="logout" class="w-50 mx-auto">
        <button type="submit" class="btn btn-danger w-100">Выйти</button>
      </form>
    </div>

    <div v-if="isSuperUser" class="mt-5">
      <h2>Список пользователей</h2>
      <ul class="list-group">
        <li class="list-group-item" v-for="user in users" :key="user.id">
          <div class="user-info">
            <div><strong>ID:</strong> {{ user.id }}</div>
            <div><strong>Имя пользователя:</strong> {{ user.username }}</div>
            <div><strong>Email:</strong> {{ user.email }}</div>
            <div><strong>Имя:</strong> {{ user.first_name }}</div>
            <div><strong>Фамилия:</strong> {{ user.last_name }}</div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.user-info {
  border: 1px solid #ccc; /* Рамка для разделения пользователей */
  border-radius: 5px; /* Скругление углов */
  padding: 10px; /* Внутренний отступ */
  margin: 10px; /* Отступ между пользователями */
  background-color: #f9f9f9; /* Цвет фона для элемента */
}

.user-info div {
  margin-bottom: 5px; /* Отступ между строками информации о пользователе */
}

.list-group-item {
  transition: background-color 0.3s; /* Плавный переход при наведении */
  padding: 5px; /* Внешний отступ */
}

.list-group-item:hover {
  background-color: #e0e0e0; /* Изменение цвета фона при наведении */
}
</style>