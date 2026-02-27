<template>
    <footer class="footer">
        <div class="footer__container">
            <div class="footer__top">
                <router-link to="/" class="footer__logo">Padarunak.by</router-link>
                <nav class="footer__nav">
                </nav>
            </div>
            <div class="footer__bottom">
                <p class="footer__copy">© {{ year }} Padarunak.by. Все права защищены.</p>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'PageFooter',
    data() {
        return {
            year: new Date().getFullYear()
        }
    }
}
</script>
