<template>
    <form class="wishlist-form" @submit.prevent="$emit('submit')">
        <h2 class="wishlist-form__title">Новый товар</h2>

        <p v-if="formError" class="wishlist-form__error">{{ formError }}</p>

        <div class="wishlist-form__field">
            <label for="wishlist-form-name">Название</label>
            <input
                id="wishlist-form-name"
                :value="form.name"
                type="text"
                required
                placeholder="Название товара"
                @input="$emit('update:form', { ...form, name: $event.target.value })"
            />
        </div>

        <div class="wishlist-form__field">
            <label for="wishlist-form-image">Картинка (URL)</label>
            <input
                id="wishlist-form-image"
                :value="form.imageUrl"
                type="url"
                placeholder="https://..."
                @input="$emit('update:form', { ...form, imageUrl: $event.target.value })"
            />
        </div>

        <div class="wishlist-form__field">
            <label for="wishlist-form-link">Ссылка</label>
            <input
                id="wishlist-form-link"
                :value="form.link"
                type="url"
                required
                placeholder="https://..."
                @input="$emit('update:form', { ...form, link: $event.target.value })"
            />
        </div>

        <div class="wishlist-form__field">
            <label for="wishlist-form-price">Цена</label>
            <input
                id="wishlist-form-price"
                :value="form.price"
                type="text"
                placeholder="Например: 99.00 BYN"
                @input="$emit('update:form', { ...form, price: $event.target.value })"
            />
        </div>

        <div class="wishlist-form__actions">
            <button type="submit" class="wishlist-form__submit" :disabled="submitting">
                {{ submitting ? 'Добавление...' : 'Добавить' }}
            </button>
            <button type="button" class="wishlist-form__cancel" :disabled="submitting" @click="$emit('cancel')">
                Отмена
            </button>
        </div>
    </form>
</template>

<script>
export default {
    name: 'WishlistForm',
    props: {
        form: {
            type: Object,
            required: true
        },
        submitting: {
            type: Boolean,
            default: false
        },
        formError: {
            type: String,
            default: null
        }
    },
    emits: ['submit', 'cancel', 'update:form']
}
</script>

<style lang="scss" src="./WishlistForm.scss" scoped></style>
