<template>
  <div class="home">
    <p v-if="error" class="home__error">{{ error }}</p>
    <template v-else-if="loading">
      <p class="home__loading">Загрузка подборок...</p>
    </template>
    <template v-else>
      <HomeCollection :collection="collectionById(1)" />
      <HomeCollection :collection="collectionById(2)" />
      <HomeCollection :collection="collectionById(3)" />
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { fetchHome } from '../../api/home'
import HomeCollection from '../../components/home/HomeCollection/HomeCollection.vue'

export default {
  name: 'HomePage',
  components: {
    HomeCollection
  },
  setup() {
    const collections = ref([])
    const loading = ref(true)
    const error = ref(null)

    function collectionById(id) {
      return collections.value.find((c) => c.id === id) || null
    }

    onMounted(async () => {
      try {
        const data = await fetchHome()
        collections.value = data.collections || []
      } catch (e) {
        error.value = e.message || 'Ошибка загрузки'
      } finally {
        loading.value = false
      }
    })

    return {
      collections,
      loading,
      error,
      collectionById
    }
  }
}
</script>

<style lang="scss" src="./Home.scss" scoped></style>
