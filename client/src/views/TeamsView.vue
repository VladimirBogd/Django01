<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

onBeforeMount(() => {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);

const teams = ref([]);
const guilds = ref([]);
const teamToAdd = ref({});
const teamToEdit = ref({});

const guildsById = computed(() => {
  return _.keyBy(guilds.value, (x) => x.id);
});

async function fetchGuilds() {
  const r = await axios.get("/api/guilds/");
  console.log(r.data);
  guilds.value = r.data;
}

async function fetchTeams() {
  loading.value = true;
  const r = await axios.get("/api/teams/");
  console.log(r.data);
  teams.value = r.data;
  loading.value = false;
}

async function onTeamAdd() {
  await axios.post("/api/teams/", {
    ...teamToAdd.value,
  });
  await fetchTeams(); // переподтягиваю
}

async function OnTeamEdit(team) {
  teamToEdit.value = { ...team };
}

async function onTeamUpdate() {
  await axios.put(`/api/teams/${teamToEdit.value.id}/`, {
    ...teamToEdit.value,
  });
  await fetchTeams();
}

async function OnTeamRemove(team) {
  console.log(team);
  await axios.delete(`/api/teams/${team.id}/`);
  await fetchTeams();
}

onBeforeMount(async () => {
  await fetchGuilds();
  await fetchTeams();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onTeamAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                v-model="teamToAdd.name"
                required
              />
              <label for="floatingInput">Название</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating mb-3">
              <select class="form-select" v-model="teamToAdd.guild" required>
                <option :value="g.id" v-for="g in guilds">{{ g.name }}</option>
              </select>
              <label for="floatingInput">Гильдия</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="item in teams" class="team-item">
          <div>{{ item.name }}</div>
          <div>{{ guildsById[item.guild]?.name }}</div>
          <button
            class="btn btn-success"
            @click="OnTeamEdit(item)"
            data-bs-toggle="modal"
            data-bs-target="#editTeamModal"
          >
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-danger" @click="OnTeamRemove(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>

      <div
        class="modal fade"
        id="editTeamModal"
        tabindex="-1"
        aria-labelledby="editTeamModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="editTeamModalLabel">
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
                      v-model="teamToEdit.name"
                    />
                    <label for="floatingInput">Название</label>
                  </div>
                </div>
                <div class="col-auto">
                  <div class="form-floating mb-3">
                    <select class="form-select" v-model="teamToEdit.guild">
                      <option :value="g.id" v-for="g in guilds">
                        {{ g.name }}
                      </option>
                    </select>
                    <label for="floatingInput">Гильдия</label>
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
                  @click="onTeamUpdate"
                >
                  Save changes
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.team-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}
</style>