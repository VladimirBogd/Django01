import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

const useUserStore = defineStore("UserStore", () => {
    const isAuthenticated = ref(false);
    const username = ref("");
    const userId = ref();

    async function fetchUser() {
        const r = await axios.get("/api/users/info/");
        isAuthenticated.value = r.data.is_authenticated;
        username.value = r.data.username;
        userId.value = r.data.user_id;
    }
    
    onBeforeMount(() => {
        fetchUser();
    })
    
    return {
        isAuthenticated,
        username,
        userId,
        fetchUser,
    };
})

export default useUserStore