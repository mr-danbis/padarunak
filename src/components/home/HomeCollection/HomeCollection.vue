<template>
    <section v-if="collection" class="home-collection">
        <h2 class="home-collection__title">{{ collection.name }}</h2>
        <ul class="home-collection__grid">
            <li
                v-for="product in collection.products"
                :key="product.id"
                class="home-collection-card"
            >
                <a
                    v-if="product.imageUrl"
                    :href="product.link"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="home-collection-card__image-wrap"
                >
                    <img
                        :src="product.imageUrl"
                        :alt="product.name"
                        class="home-collection-card__image"
                        loading="lazy"
                    />
                </a>
                <div v-else class="home-collection-card__image-wrap home-collection-card__image-wrap_placeholder" />
                <div class="home-collection-card__body">
                    <a
                        :href="product.link"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="home-collection-card__name"
                    >
                        {{ product.name }}
                    </a>
                    <p v-if="product.price" class="home-collection-card__price">{{ product.price }}</p>
                    <router-link :to="{ path: '/account', query: { section: 'wishlist' } }" class="home-collection-card__btn">
                        В вишлист
                    </router-link>
                </div>
            </li>
        </ul>
    </section>
</template>

<script>
export default {
    name: 'HomeCollection',
    props: {
        collection: {
            type: Object,
            default: null
        }
    }
}
</script>

<style lang="scss" src="./HomeCollection.scss" scoped></style>
