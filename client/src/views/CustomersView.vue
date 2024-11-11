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

async function fetchCustomers() {
  loading.value = true;
  const r = await axios.get("/api/customers/");
  console.log(r.data);
  customers.value = r.data;
  loading.value = false;
}

async function onCustomerAdd() {
  await axios.post("/api/customers/", {
    ...customerToAdd.value,
  });
  await fetchCustomers(); // переподтягиваю
}

async function OnCustomerRemove(customer) {
  console.log(customer);
  await axios.delete(`/api/customers/${customer.id}/`);
  await fetchCustomers();
}

async function OnCustomerEdit(customer) {
  customerToEdit.value = { ...customer };
}

async function onCustomerUpdate() {
  await axios.put(`/api/customers/${customerToEdit.value.id}/`, {
    ...customerToEdit.value,
  });
  await fetchCustomers();
}

onBeforeMount(async () => {
  await fetchCustomers();
});
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
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="item in customers" class="customer-item">
          <div>{{ item.name }}</div>
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
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}
</style>