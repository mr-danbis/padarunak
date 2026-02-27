<template>
    <div class="wishlist">
        <div class="wishlist__container">
            <h1 class="wishlist__title">Мой вишлист</h1>

            <p v-if="error" class="wishlist__error">
                {{ error }}
                <button type="button" class="wishlist__retry" @click="fetchWishlist">Повторить</button>
            </p>

            <template v-if="!showForm">
                <div class="wishlist__by-link">
                    <label for="wishlist-link-input" class="wishlist__by-link-label">Добавить по ссылке</label>
                    <div class="wishlist__by-link-row">
                        <input
                            id="wishlist-link-input"
                            v-model="linkUrl"
                            type="url"
                            class="wishlist__by-link-input"
                            placeholder="Вставьте ссылку на товар"
                            :disabled="linkLoading"
                            @keydown.enter.prevent="fetchPreview"
                        />
                        <button
                            type="button"
                            class="wishlist__by-link-btn"
                            :disabled="linkLoading || !linkUrlTrimmed"
                            @click="fetchPreview"
                        >
                            {{ linkLoading ? 'Загрузка...' : 'Подтянуть данные' }}
                        </button>
                    </div>
                    <p v-if="linkError" class="wishlist__by-link-error">{{ linkError }}</p>
                    <div v-if="linkPreview" class="wishlist__preview">
                        <div class="wishlist__preview-inner">
                            <img
                                v-if="linkPreview.imageUrl"
                                :src="linkPreview.imageUrl"
                                :alt="linkPreview.name"
                                class="wishlist__preview-img"
                            />
                            <div v-else class="wishlist__preview-img wishlist__preview-img_placeholder" />
                            <div class="wishlist__preview-body">
                                <span class="wishlist__preview-name">{{ linkPreview.name }}</span>
                                <span v-if="linkPreview.price" class="wishlist__preview-price">{{ linkPreview.price }}</span>
                                <div class="wishlist__preview-actions">
                                    <button
                                        type="button"
                                        class="wishlist__preview-add"
                                        :disabled="addingFromPreview"
                                        @click="addFromPreview"
                                    >
                                        {{ addingFromPreview ? 'Добавление...' : 'Добавить в вишлист' }}
                                    </button>
                                    <button
                                        type="button"
                                        class="wishlist__preview-cancel"
                                        :disabled="addingFromPreview"
                                        @click="clearLinkPreview"
                                    >
                                        Отмена
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
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
import { ref, computed, onMounted } from 'vue'
import { useWishlist } from '../../composables/useWishlist'
import { useWishlistForm } from '../../composables/useWishlistForm'
import { fetchLinkPreview } from '../../api/wishlist'
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

        const linkUrl = ref('')
        const linkLoading = ref(false)
        const linkError = ref(null)
        const linkPreview = ref(null)
        const addingFromPreview = ref(false)

        const linkUrlTrimmed = computed(() => linkUrl.value.trim())

        async function fetchPreview() {
            const url = linkUrlTrimmed.value
            if (!url) return
            linkError.value = null
            linkPreview.value = null
            linkLoading.value = true
            try {
                linkPreview.value = await fetchLinkPreview(url)
            } catch (e) {
                linkError.value = e.message || 'Не удалось загрузить данные по ссылке'
            } finally {
                linkLoading.value = false
            }
        }

        async function addFromPreview() {
            if (!linkPreview.value) return
            addingFromPreview.value = true
            linkError.value = null
            try {
                await addItem({
                    name: linkPreview.value.name,
                    imageUrl: linkPreview.value.imageUrl || undefined,
                    link: linkPreview.value.link,
                    price: linkPreview.value.price || undefined
                })
                clearLinkPreview()
            } catch (e) {
                linkError.value = e.message || 'Не удалось добавить товар'
            } finally {
                addingFromPreview.value = false
            }
        }

        function clearLinkPreview() {
            linkPreview.value = null
            linkError.value = null
            linkUrl.value = ''
        }

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
            removeItem,
            linkUrl,
            linkUrlTrimmed,
            linkLoading,
            linkError,
            linkPreview,
            addingFromPreview,
            fetchPreview,
            addFromPreview,
            clearLinkPreview
        }
    }
}
</script>

<style lang="scss" src="./Wishlist.scss" scoped></style>
