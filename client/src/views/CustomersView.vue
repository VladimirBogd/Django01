<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

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
  const formData = new FormData();

  formData.append("picture", customerAddPictureRef.value.files[0]);

  formData.set("name", customerToAdd.value.name);

  await axios.post("/api/customers/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  await fetchCustomers(); // переподтягиваю
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

  if (!hasCustomerEditPicture.value) {
    formData.set("picture", "");
  } else if (customerEditPictureRef.value.files[0]) {
    formData.set("picture", customerEditPictureRef.value.files[0]);
  }

  formData.set("name", customerToEdit.value.name);

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
}

async function OnCustomerRemove(customer) {
  console.log(customer);
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
      <form @submit.prevent.stop="onCustomerAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                v-model="customerToAdd.name"
                required
              />
              <label for="floatingInput">Название</label>
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
              @click="showZoomImage(customerAddImageUrl)"
            />
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="item in customers" class="customer-item">
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
                      v-model="customerToEdit.name"
                    />
                    <label for="floatingInput">Название</label>
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
                Close
              </button>
              <button
                type="button"
                class="btn btn-primary"
                data-bs-dismiss="modal"
                @click="onCustomerUpdate"
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