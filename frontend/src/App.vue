<template>
  <div class="app-layout">
    <PageHeader />
    <main class="app-layout__main">
      <div class="app-layout__container">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
    <PageFooter />
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useWishlistStore } from './stores/wishlistStore'
import { useAuthStore } from './stores/authStore'
import PageHeader from './components/common/PageHeader/PageHeader.vue'
import PageFooter from './components/common/PageFooter/PageFooter.vue'

export default {
  name: 'App',
  components: {
    PageHeader,
    PageFooter
  },
  setup() {
    const authStore = useAuthStore()
    const wishlistStore = useWishlistStore()
    onMounted(async () => {
      await authStore.fetchUser()
      if (authStore.isLoggedIn) {
        wishlistStore.fetchWishlist()
      }
    })
  }
}
</script>
