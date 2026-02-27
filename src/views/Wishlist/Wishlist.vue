<template>
    <div class="wishlist">
        <div class="wishlist__container">
            <h1 class="wishlist__title">Мой вишлист</h1>

            <p v-if="error" class="wishlist__error">
                {{ error }}
                <button type="button" class="wishlist__retry" @click="fetchWishlist">Повторить</button>
            </p>

            <template v-if="!showForm">
                <button
                    type="button"
                    class="wishlist__add-btn"
                    :disabled="loading"
                    @click="openForm"
                >
                    {{ loading ? 'Загрузка...' : 'Добавить вручную' }}
                </button>
            </template>

            <transition name="fade">
                <WishlistForm
                    v-if="showForm"
                    :form="form"
                    :submitting="submitting"
                    :form-error="formError"
                    @submit="onSubmit"
                    @cancel="closeForm"
                    @update:form="assignForm"
                />
            </transition>

            <div v-if="!loading && items.length === 0 && !showForm" class="wishlist__empty">
                Вишлист пуст. Нажмите «Добавить вручную», чтобы добавить первый товар.
            </div>

            <ul v-else-if="items.length > 0" class="wishlist__list">
                <WishlistItem
                    v-for="item in items"
                    :key="item.id"
                    :item="item"
                    @remove="removeItem(item.id)"
                />
            </ul>
        </div>
    </div>
</template>

<script>
import { onMounted } from 'vue'
import { useWishlist } from '../../composables/useWishlist'
import { useWishlistForm } from '../../composables/useWishlistForm'
import WishlistForm from '../../components/wishlist/WishlistForm/WishlistForm.vue'
import WishlistItem from '../../components/wishlist/WishlistItem/WishlistItem.vue'

export default {
    name: 'WishlistPage',
    components: {
        WishlistForm,
        WishlistItem
    },
    setup() {
        const { items, loading, error, fetchWishlist, addItem, removeItem } = useWishlist()
        const { showForm, form, submitting, error: formError, onSubmit, openForm, closeForm } = useWishlistForm(addItem)

        onMounted(() => {
            fetchWishlist()
        })

        function assignForm(payload) {
            Object.assign(form, payload)
        }

        return {
            items,
            loading,
            error,
            fetchWishlist,
            showForm,
            form,
            submitting,
            formError,
            onSubmit,
            openForm,
            closeForm,
            assignForm,
            removeItem
        }
    }
}
</script>

<style lang="scss" src="./Wishlist.scss" scoped></style>
