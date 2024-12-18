<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

import { useRouter } from "vue-router";
import useUserStore from "@/stores/userStore";

const userStore = useUserStore();
// Проверка, вошел ли пользователь в систему
const isLoggedIn = computed(() => userStore.isAuthenticated);
const isSuperUser = computed(() => userStore.isSuperUser);

onBeforeMount(() => {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);

const customers = ref([]);
const customerToAdd = ref({});
const customerToEdit = ref({});

const customerAddPictureRef = ref();
const customerEditPictureRef = ref();
const customerAddImageUrl = ref();
const customerEditImageUrl = ref();
const hasCustomerEditPicture = ref(false);

async function fetchCustomers() {
  loading.value = true;
  const r = await axios.get("/api/customers/");
  console.log(r.data);
  customers.value = r.data;
  loading.value = false;
}

async function onCustomerAdd() {
  console.log(customerToAdd.value); // Для отладки
  const formData = new FormData();

  if (customerAddPictureRef.value.files[0]) {
    formData.set("picture", customerAddPictureRef.value.files[0]);
  }

  formData.set("username", customerToAdd.value.username);
  formData.set("email", customerToAdd.value.email);
  formData.set("password", customerToAdd.value.password);

  // Логируем данные FormData
  for (const [key, value] of formData.entries()) {
      console.log(key, value);
  }

  try {
    await axios.post("/api/customers/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    await fetchCustomers();
  } catch (error) {
      console.error("Ошибка при создании клиента:", error);
  }
}

async function customerAddPictureChange() {
  customerAddImageUrl.value = URL.createObjectURL(
    customerAddPictureRef.value.files[0]
  );
}

async function OnCustomerEdit(customer) {
  customerToEdit.value = { ...customer };
  customerEditImageUrl.value = customer.picture;
}

async function onCustomerUpdate() {
  const formData = new FormData();

  if (hasCustomerEditPicture.value && customerEditPictureRef.value.files[0]) {
    formData.set("picture", customerEditPictureRef.value.files[0]);
  } else {
    formData.set("picture", "");
  }

  formData.set("username", customerToEdit.value.username);
  formData.set("email", customerToEdit.value.email);

  await axios.put(`/api/customers/${customerToEdit.value.id}/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  await fetchCustomers();
}

async function customerEditPictureChange() {
  customerEditImageUrl.value = URL.createObjectURL(
    customerEditPictureRef.value.files[0]
  );
  hasCustomerEditPicture.value = true;
}

async function OnCustomerRemove(customer) {
  await axios.delete(`/api/customers/${customer.id}/`);
  await fetchCustomers();
}

onBeforeMount(async () => {
  await fetchCustomers();
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
      <div v-if="isLoggedIn">
        <form v-if="isSuperUser" @submit.prevent.stop="onCustomerAdd">
          <div class="row">
            <div class="col">
              <div class="form-floating mb-3">
                <input
                  type="text"
                  class="form-control"
                  v-model="customerToAdd.username"
                  required
                />
                <label for="floatingInput">Имя пользователя</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating mb-3">
                <input
                  type="email"
                  class="form-control"
                  v-model="customerToAdd.email"
                  required
                />
                <label for="floatingInput">Электронная почта</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating mb-3">
                <input
                  type="password"
                  class="form-control"
                  v-model="customerToAdd.password"
                  required
                />
                <label for="floatingInput">Пароль</label>
              </div>
            </div>
            <div class="col-auto">
              <input
                class="form-control"
                type="file"
                ref="customerAddPictureRef"
                @change="customerAddPictureChange"
              />
            </div>
            <div class="col-auto">
              <img
                :src="customerAddImageUrl"
                style="max-height: 60px"
                alt="Изображение"
                v-if="customerAddImageUrl"
                @click="showZoomImage(customerAddImageUrl)"
              />
            </div>
            <div class="col-auto">
              <button class="btn btn-primary">Добавить</button>
            </div>
          </div>
        </form>

        <div v-if="loading">Гружу...</div>

        <div v-if="isSuperUser">
          <div v-for="item in customers" :key="item.id" class="customer-item">
            <div>{{ item.username }}</div>
            <div>{{ item.email }}</div>
            <div v-show="item.picture">
              <img
                :src="item.picture"
                style="max-height: 60px"
                @click="showZoomImage(item.picture)"
              />
            </div>
            <button
              class="btn btn-success"
              @click="OnCustomerEdit(item)"
              data-bs-toggle="modal"
              data-bs-target="#editCustomerModal"
            >
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-danger" @click="OnCustomerRemove(item)">
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>

        <div
          class="modal fade"
          id="editCustomerModal"
          tabindex="-1"
          aria-labelledby="editCustomerModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="editCustomerModalLabel">
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
                        v-model="customerToEdit.username"
                      />
                      <label for="floatingInput">Имя пользователя</label>
                    </div>
                    <div class="form-floating mb-3">
                      <input
                        type="email"
                        class="form-control"
                        v-model="customerToEdit.email"
                      />
                      <label for="floatingInput">Электронная почта</label>
                    </div>
                    <div class="col-auto">
                      <input
                        class="form-control"
                        type="file"
                        ref="customerEditPictureRef"
                        @change="customerEditPictureChange"
                      />
                    </div>
                    <div class="col-auto">
                      <button
                        class="btn btn-danger"
                        @click="
                          hasCustomerEditPicture = false;
                          customerEditImageUrl = '';
                        "
                      >
                        Очистить
                      </button>
                    </div>
                    <div class="col-auto">
                      <img
                        :src="customerEditImageUrl"
                        style="max-height: 60px"
                        alt="Изображение"
                      />
                    </div>
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
                  @click="onCustomerUpdate"
                >
                  Сохранить изменения
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
      <div v-else>Вы не авторизованы</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.customer-item {
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