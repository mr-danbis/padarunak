import { ref, reactive } from 'vue'

const defaultForm = () => ({
  name: '',
  imageUrl: '',
  link: '',
  price: ''
})

export function useWishlistForm(addItem) {
  const showForm = ref(false)
  const form = reactive(defaultForm())
  const submitting = ref(false)
  const error = ref(null)

  async function onSubmit() {
    error.value = null
    submitting.value = true
    try {
      await addItem({
        name: form.name.trim(),
        imageUrl: form.imageUrl.trim() || undefined,
        link: form.link.trim(),
        price: form.price.trim() || undefined
      })
      Object.assign(form, defaultForm())
      showForm.value = false
    } catch (e) {
      error.value = e.message || 'Ошибка при добавлении'
    } finally {
      submitting.value = false
    }
  }

  function openForm() {
    showForm.value = true
    error.value = null
  }

  function closeForm() {
    showForm.value = false
    error.value = null
  }

  return {
    showForm,
    form,
    submitting,
    error,
    onSubmit,
    openForm,
    closeForm
  }
}
