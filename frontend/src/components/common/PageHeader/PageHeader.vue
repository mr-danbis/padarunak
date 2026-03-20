<template>
  <header class="header">
    <div class="header__container">
      <router-link to="/" class="header__logo">wishka</router-link>
      <div v-if="!authLoading" class="header__right">
        <template v-if="user">
          <router-link to="/account" class="header__avatar-link">
            <img
              v-if="user.pictureUrl && !avatarImgError"
              :src="user.pictureUrl"
              :alt="user.name || user.email"
              class="header__avatar-img"
              @error="avatarImgError = true"
            />
            <span v-else class="header__avatar-placeholder">{{ userInitial }}</span>
          </router-link>
        </template>
        <button v-else type="button" class="header__login" @click="login">Войти</button>
      </div>
    </div>
  </header>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../../../stores/authStore'

export default {
  name: 'PageHeader',
  setup() {
    const authStore = useAuthStore()
    const { user, loading: authLoading } = storeToRefs(authStore)
    const avatarImgError = ref(false)

    const userInitial = computed(() => {
      const u = user.value
      if (!u) return '?'
      const name = u.name || u.email || ''
      return name.charAt(0).toUpperCase() || '?'
    })

    watch(
      () => user.value?.pictureUrl,
      () => {
        avatarImgError.value = false
      }
    )

    return {
      user,
      authLoading,
      userInitial,
      avatarImgError,
      login: () => authStore.login()
    }
  }
}
</script>

<style lang="scss" src="./PageHeader.scss" scoped></style>
