<template>
    <li class="wishlist-item">
        <a
            :href="item.link"
            target="_blank"
            rel="noopener noreferrer"
            class="wishlist-item__link"
        >
            <div class="wishlist-item__image-wrap">
                <img
                    v-if="item.imageUrl"
                    :src="item.imageUrl"
                    :alt="item.name"
                    class="wishlist-item__image"
                    loading="lazy"
                />
            </div>
            <div class="wishlist-item__body">
                <span class="wishlist-item__name">{{ item.name }}</span>
                <p v-if="item.price" class="wishlist-item__price">{{ item.price }}</p>
            </div>
        </a>
        <button
            type="button"
            class="wishlist-item__remove"
            aria-label="Удалить"
            @click.stop="$emit('remove')"
        >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                <line x1="10" y1="11" x2="10" y2="17" />
                <line x1="14" y1="11" x2="14" y2="17" />
            </svg>
        </button>
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
