<script setup>
import { storeToRefs } from "pinia";
import useUserStore from "./stores/userStore";

const userStore = useUserStore();
const { isSuperUser, isAuthenticated, username, userId } = storeToRefs(userStore);
</script>

<template>
  
  <div>
    <nav class="navbar sticky-top navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid navbar-mine">
        <a class="navbar-brand" href="#">Fairy Fairy</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/"> Волшебники </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/guilds"> Гильдии </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/teams"> Команды </router-link>
            </li>
            <li v-if="isSuperUser" class="nav-item">
              <router-link class="nav-link" to="/customers">
                Заказчики
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/orders"> Заказы </router-link>
            </li>
          </ul>
          <form class="d-flex">
            <ul class="navbar-nav">
              <li class="nav-item dropdown" style="margin-right: 50px">
                <a
                  class="nav-link dropdown-toggle"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ username }}
                </a>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="/admin">Админка</a></li>
                </ul>
              </li>
            </ul>
            <router-link class="nav-link" to="/users">
              <button class="btn btn-outline-info" type="button">
                <i class="bi bi-person-fill"></i>
              </button>
            </router-link>
          </form>
        </div>
      </div>
    </nav>
    <div>
      <router-view />
    </div>

  </div>
</template>

<style scoped>
.navbar-mine {
  padding: 0 1.25rem 0 1.25rem;
}
</style>