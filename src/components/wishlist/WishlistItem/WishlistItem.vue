<template>
    <li class="wishlist-item">
        <a
            v-if="item.imageUrl"
            :href="item.link"
            target="_blank"
            rel="noopener noreferrer"
            class="wishlist-item__image-wrap"
        >
            <img
                :src="item.imageUrl"
                :alt="item.name"
                class="wishlist-item__image"
                loading="lazy"
            />
        </a>
        <div class="wishlist-item__body">
            <a
                :href="item.link"
                target="_blank"
                rel="noopener noreferrer"
                class="wishlist-item__name"
            >
                {{ item.name }}
            </a>
            <p v-if="item.price" class="wishlist-item__price">
                {{ item.price }}
            </p>
            <button
                type="button"
                class="wishlist-item__remove"
                aria-label="Удалить"
                @click="$emit('remove')"
            >
                Удалить
            </button>
        </div>
    </li>
</template>

<script>
export default {
    name: 'WishlistItem',
    props: {
        item: {
            type: Object,
            required: true
        }
    },
    emits: ['remove']
}
</script>

<style lang="scss" src="./WishlistItem.scss" scoped></style>
