<template>
    <header class="header">
        <div class="header__container">
            <router-link to="/" class="header__logo">
                Padarunak.by
            </router-link>
            <ul class="header__menu">
                <li>
                    <router-link to="/wishlist" class="header__wishlist-link">
                        Вишлист
                        <span v-if="wishlistCount > 0" class="header__wishlist-count">{{ wishlistCount }}</span>
                    </router-link>
                </li>
            </ul>
        </div>
    </header>
</template>

<script>
    import { storeToRefs } from 'pinia'
    import { useWishlistStore } from '../../../stores/wishlistStore'

    export default {
        name: 'PageHeader',
        setup() {
            const wishlistStore = useWishlistStore()
            const { wishlistCount } = storeToRefs(wishlistStore)
            return { wishlistCount }
        }
    }
</script>