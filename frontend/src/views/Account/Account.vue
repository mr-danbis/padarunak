<template>
    <div class="account">
        <aside class="account__sidebar">
            <nav class="account__nav">
                <router-link
                    :to="{ path: '/account', query: {} }"
                    class="account__nav-link"
                    :class="{ 'account__nav-link_active': section !== 'wishlist' }"
                >
                    Моя информация
                </router-link>
                <router-link
                    :to="{ path: '/account', query: { section: 'wishlist' } }"
                    class="account__nav-link"
                    :class="{ 'account__nav-link_active': section === 'wishlist' }"
                >
                    Мой вишлист
                    <span v-if="wishlistCount > 0" class="account__nav-count">{{ wishlistCount }}</span>
                </router-link>
            </nav>
        </aside>
        <div class="account__content">
            <div v-if="section !== 'wishlist'" class="account__section">
                <h1 class="section-title">Моя информация</h1>
                <div v-if="user" class="account__profile">
                    <img
                        v-if="user.pictureUrl && !avatarImgError"
                        :src="user.pictureUrl"
                        :alt="user.name"
                        class="account__avatar"
                        @error="avatarImgError = true"
                    />
                    <div v-else class="account__avatar account__avatar_placeholder">{{ userInitial }}</div>
                    <p v-if="firstName" class="account__field"><span class="account__label">Имя</span> {{ firstName }}</p>
                    <p v-if="lastName" class="account__field"><span class="account__label">Фамилия</span> {{ lastName }}</p>
                    <p v-if="user.email" class="account__field"><span class="account__label">Почта</span> {{ user.email }}</p>
                </div>
                <button type="button" class="account__logout" @click="logout">Выйти</button>
            </div>
            <Wishlist v-else class="account__wishlist" />
        </div>
    </div>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../../stores/authStore'
import { useWishlistStore } from '../../stores/wishlistStore'
import Wishlist from '../Wishlist/Wishlist.vue'

function splitFullName(fullName) {
    if (!fullName || typeof fullName !== 'string') return { firstName: '', lastName: '' }
    const parts = fullName.trim().split(/\s+/)
    if (parts.length === 0) return { firstName: '', lastName: '' }
    if (parts.length === 1) return { firstName: parts[0], lastName: '' }
    return {
        firstName: parts[0],
        lastName: parts.slice(1).join(' ')
    }
}

export default {
    name: 'AccountPage',
    components: {
        Wishlist
    },
    setup() {
        const route = useRoute()
        const authStore = useAuthStore()
        const wishlistStore = useWishlistStore()
        const { user } = storeToRefs(authStore)
        const { wishlistCount } = storeToRefs(wishlistStore)

        const section = computed(() => route.query.section || 'info')
        const avatarImgError = ref(false)
        watch(() => user.value?.pictureUrl, () => { avatarImgError.value = false })
        const firstName = computed(() => (user.value ? splitFullName(user.value.name).firstName : ''))
        const lastName = computed(() => (user.value ? splitFullName(user.value.name).lastName : ''))
        const userInitial = computed(() => {
            const u = user.value
            if (!u) return '?'
            const n = u.name || u.email || ''
            return n.charAt(0).toUpperCase() || '?'
        })

        return {
            user,
            wishlistCount,
            section,
            firstName,
            lastName,
            userInitial,
            avatarImgError,
            logout: () => authStore.logout()
        }
    }
}
</script>

<style lang="scss" src="./Account.scss" scoped></style>
