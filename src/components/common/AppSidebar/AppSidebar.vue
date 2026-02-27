<template>
    <aside class="sidebar">
        <nav class="sidebar__nav">
            <router-link to="/wishlist" class="sidebar__link">
                Мой вишлист
                <span v-if="wishlistCount > 0" class="sidebar__count">{{ wishlistCount }}</span>
            </router-link>
        </nav>
    </aside>
</template>

<script>
import { storeToRefs } from 'pinia'
import { useWishlistStore } from '../../../stores/wishlistStore'

export default {
    name: 'AppSidebar',
    setup() {
        const wishlistStore = useWishlistStore()
        const { wishlistCount } = storeToRefs(wishlistStore)
        return { wishlistCount }
    }
}
</script>

<style lang="scss" src="./AppSidebar.scss" scoped></style>
