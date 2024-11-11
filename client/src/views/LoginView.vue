<!-- <script>
import router from '@/router';
import { useRouter } from 'vue-router';

    const username = ref("");
    const pass = ref("");

    async function login() {
        const r = await axios.post("/api/user/login", {
            user: username.value,
            pass: pass.value,
        })
        await userStore.fetchUser();

        router.push("/")
    }
</script>

<template>
    <input v-model="username">
    <input type="password" v-model="pass">
    
</template> -->