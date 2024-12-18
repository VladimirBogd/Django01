<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

onBeforeMount(() => {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);

const guilds = ref([]);
const guildToAdd = ref({});
const guildToEdit = ref({});

const guildAddPictureRef = ref();
const guildEditPictureRef = ref();
const guildAddImageUrl = ref();
const guildEditImageUrl = ref();
const hasGuildEditPicture = ref(false);

async function fetchGuilds() {
  loading.value = true;
  const r = await axios.get("/api/guilds/");
  console.log(r.data);
  guilds.value = r.data;
  loading.value = false;
}

async function onGuildAdd() {
  const formData = new FormData();
  
  if (guildAddPictureRef.value.files[0]) {
    formData.set("picture", guildAddPictureRef.value.files[0]);
  }

  formData.set("name", guildToAdd.value.name);

  await axios.post("/api/guilds/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  await fetchGuilds(); // переподтягиваю
}

async function guildAddPictureChange() {
  guildAddImageUrl.value = URL.createObjectURL(
    guildAddPictureRef.value.files[0]
  );
}

async function OnGuildEdit(guild) {
  guildToEdit.value = { ...guild };
  guildEditImageUrl.value = guild.picture;
}

async function onGuildUpdate() {
  const formData = new FormData();

  if (hasGuildEditPicture.value && guildEditPictureRef.value.files[0]) {
    formData.set("picture", guildEditPictureRef.value.files[0]);
  } else {
    formData.set("picture", "");
  }

  formData.set("name", guildToEdit.value.name);

  await axios.put(`/api/guilds/${guildToEdit.value.id}/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  await fetchGuilds();
}

async function guildEditPictureChange() {
  guildEditImageUrl.value = URL.createObjectURL(
    guildEditPictureRef.value.files[0]
  );
  hasGuildEditPicture.value = true;
}

async function OnGuildRemove(guild) {
  console.log(guild);
  await axios.delete(`/api/guilds/${guild.id}/`);
  await fetchGuilds();
}

onBeforeMount(async () => {
  await fetchGuilds();
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
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onGuildAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                v-model="guildToAdd.name"
                required
              />
              <label for="floatingInput">Название</label>
            </div>
          </div>
          <div class="col-auto">
            <input
              class="form-control"
              type="file"
              ref="guildAddPictureRef"
              @change="guildAddPictureChange"
            />
          </div>
          <div class="col-auto">
            <img
              :src="guildAddImageUrl"
              style="max-height: 60px"
              alt="Изображение"
              @click="showZoomImage(guildAddImageUrl)"
            />
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="item in guilds" :key="item.id" class="guild-item">
          <div>{{ item.name }}</div>
          <div v-show="item.picture">
            <img
              :src="item.picture"
              style="max-height: 60px"
              @click="showZoomImage(item.picture)"
            />
          </div>
          <button
            class="btn btn-success"
            @click="OnGuildEdit(item)"
            data-bs-toggle="modal"
            data-bs-target="#editGuildModal"
          >
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-danger" @click="OnGuildRemove(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>

      <div
        class="modal fade"
        id="editGuildModal"
        tabindex="-1"
        aria-labelledby="editGuildModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="editGuildModalLabel">
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
                      v-model="guildToEdit.name"
                    />
                    <label for="floatingInput">Название</label>
                  </div>
                </div>
                <div class="col-auto">
                  <input
                    class="form-control"
                    type="file"
                    ref="guildEditPictureRef"
                    @change="guildEditPictureChange"
                  />
                </div>
                <div class="col-auto">
                  <button
                    class="btn btn-danger"
                    @click="
                      hasGuildEditPicture = false;
                      guildEditImageUrl = '';
                    "
                  >
                    Очистить
                  </button>
                </div>
                <div class="col-auto">
                  <img
                    :src="guildEditImageUrl"
                    style="max-height: 60px"
                    alt="Изображение"
                  />
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
                  @click="onGuildUpdate"
                >
                  Save changes
                </button>
              </div>
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
.guild-item {
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