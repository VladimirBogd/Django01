<script setup>
import { computed, onBeforeMount, ref, defineProps, watch } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

onBeforeMount(() => {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);

const guilds = ref([]);
const teams = ref([]);
const wizards = ref([]);
const wizardToAdd = ref({});
const wizardToEdit = ref({});

const selectedGuild = ref(null); // Хранит выбранную гильдию
const filteredTeams = ref([]); // Хранит команды, привязанные к выбранной гильдии

const wizardAddPictureRef = ref();
const wizardEditPictureRef = ref();
const wizardAddImageUrl = ref();
const wizardEditImageUrl = ref();
const hasWizardEditPicture = ref(false);

const guildsById = computed(() => {
  return _.keyBy(guilds.value, (x) => x.id);
});

async function fetchGuilds() {
  const r = await axios.get("/api/guilds/");
  guilds.value = r.data;
}

const teamsById = computed(() => {
  return _.keyBy(teams.value, (x) => x.id);
});

async function fetchTeams() {
  const r = await axios.get("/api/teams/");
  teams.value = r.data;
}

async function fetchWizards() {
  loading.value = true;
  const r = await axios.get("/api/wizards/");
  console.log(r.data);
  wizards.value = r.data;
  loading.value = false;
}

async function onWizardAdd() {
  const formData = new FormData();

  if (wizardAddPictureRef.value.files[0]) {
    formData.set("picture", wizardAddPictureRef.value.files[0]);
  }

  formData.set("name", wizardToAdd.value.name);
  formData.set("guild", wizardToAdd.value.guild);

  // Проверяем, задано ли значение team, и добавляем его
  if (wizardToAdd.value.team) {
    formData.set("team", wizardToAdd.value.team);
  }

  try {
    await axios.post("/api/wizards/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    await fetchWizards();
    await fetchTeams();
  } catch (error) {
    console.error("Ошибка при создании волшебника:", error);
  }
}

async function wizardsAddPictureChange() {
  wizardAddImageUrl.value = URL.createObjectURL(
    wizardAddPictureRef.value.files[0]
  );
}

async function OnWizardEdit(wizard) {
  wizardToEdit.value = { ...wizard };
  wizardEditImageUrl.value = wizard.picture;
}

async function onWizardUpdate() {
  const formData = new FormData();

  if (hasWizardEditPicture.value && wizardEditPictureRef.value.files[0]) {
    formData.set("picture", wizardEditPictureRef.value.files[0]);
  } else {
    formData.set("picture", "");
  }

  formData.set("name", wizardToEdit.value.name);
  formData.set("guild", wizardToEdit.value.guild);
  if (wizardToEdit.value.team) {
    formData.set("team", wizardToEdit.value.team);
  }

  await axios.put(`/api/wizards/${wizardToEdit.value.id}/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  await fetchWizards();
  await fetchTeams();
}

async function wizardEditPictureChange() {
  wizardEditImageUrl.value = URL.createObjectURL(
    wizardEditPictureRef.value.files[0]
  );
  hasWizardEditPicture.value = true;
}

async function OnWizardRemove(wizard) {
  await axios.delete(`/api/wizards/${wizard.id}/`);
  await fetchWizards();
}

onBeforeMount(async () => {
  await fetchWizards();
  await fetchGuilds();
  await fetchTeams();
});

const showZoomImageContainer = ref(false);
const zoomImageUrl = ref("");

function showZoomImage(imageUrl) {
  zoomImageUrl.value = imageUrl;
  showZoomImageContainer.value = true;
}

function hideZoomImage() {
  showZoomImageContainer.value = false;
}

function updateTeams() {
  if (selectedGuild.value) {
    filteredTeams.value = teams.value.filter(
      (team) => team.guild === selectedGuild.value
    );
    wizardToAdd.value.guild = selectedGuild.value;
  } else {
    filteredTeams.value = []; // Если гильдия не выбрана, очищаем команды
  }
}
// Устанавливаем реактивный обработчик для выбора гильдии
watch(selectedGuild, updateTeams);
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onWizardAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                v-model="wizardToAdd.name"
                required
              />
              <label for="floatingInput">ФИО</label>
            </div>
          </div>
          <div class="col-auto">
            <input
              class="form-control"
              type="file"
              ref="wizardAddPictureRef"
              @change="wizardsAddPictureChange"
            />
          </div>
          <div class="col-auto">
            <img
              :src="wizardAddImageUrl"
              style="max-height: 60px"
              alt="Изображение"
              @click="showZoomImage(wizardAddImageUrl)"
            />
          </div>
          <div class="col-auto">
            <div class="form-floating mb-3">
              <select
                class="form-select"
                v-model="selectedGuild"
                @change="updateTeams"
                required
              >
                <option v-for="g in guilds" :key="g.id" :value="g.id">
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
                v-model="wizardToAdd.team"
                :disabled="!selectedGuild"
                required
              >
                <option :value="null">Нет команды</option>
                <option v-for="t in filteredTeams" :key="t.id" :value="t.id">
                  {{ t.name }}
                </option>
              </select>
              <label for="floatingInput">Команда</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="item in wizards" :key="item.id" class="wizard-item">
          <div>{{ item.name }}</div>
          <div>{{ guildsById[item.guild]?.name }}</div>
          <div>{{ teamsById[item.team]?.name }}</div>
          <div v-show="item.picture">
            <img
              :src="item.picture"
              style="max-height: 60px"
              @click="showZoomImage(item.picture)"
            />
          </div>
          <button
            class="btn btn-success"
            @click="OnWizardEdit(item)"
            data-bs-toggle="modal"
            data-bs-target="#editWizardModal"
          >
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-danger" @click="OnWizardRemove(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>

      <div
        class="modal fade"
        id="editWizardModal"
        tabindex="-1"
        aria-labelledby="editWizardModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="editWizardModalLabel">
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
                      v-model="wizardToEdit.name"
                    />
                    <label for="floatingInput">ФИО</label>
                  </div>
                </div>
                <div class="col-auto">
                  <div class="form-floating mb-3">
                    <select
                      class="form-select"
                      v-model="wizardToEdit.guild"
                    >
                      <option v-for="g in guilds" :key="g.id" :value="g.id">
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
                      v-model="wizardToEdit.team"
                    >
                      <option :value="null">Нет команды</option>
                      <option v-for="t in teams" :key="t.id" :value="t.id">
                        {{ t.name }}
                      </option>
                    </select>
                    <label for="floatingInput">Команда</label>
                  </div>
                </div>
                <div class="col-auto">
                  <input
                    class="form-control"
                    type="file"
                    ref="wizardEditPictureRef"
                    @change="wizardEditPictureChange"
                  />
                </div>
                <div class="col-auto">
                  <button
                    class="btn btn-danger"
                    @click="
                      hasWizardEditPicture = false;
                      wizardEditImageUrl = '';
                    "
                  >
                    Очистить
                  </button>
                </div>
                <div class="col-auto">
                  <img
                    :src="wizardEditImageUrl"
                    style="max-height: 60px"
                    alt="Изображение"
                  />
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
                @click="onWizardUpdate"
              >
                Save changes
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="zoom-image-container"
        :class="{ active: showZoomImageContainer }"
        @click="hideZoomImage"
      >
        <img :src="zoomImageUrl" alt="Увеличенное изображение" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.wizard-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}

img {
  cursor: pointer;
}

.zoom-image-container {
  position: fixed;
  left: 0;
  top: 40px;
  right: 0;
  bottom: 0;
  display: block;
  padding: 1rem;
  backdrop-filter: blur(4px);
  z-index: 100;
  transform: scale(0.2, 0.2);
  transition: all 0.2s ease-out;
  opacity: 0;
  height: 0;
  overflow: hidden;
}

.zoom-image-container.active {
  opacity: 1;
  transform: scale(1, 1);
  height: auto;
}

.zoom-image-container img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
</style>
