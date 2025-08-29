<template>
    <div class="header">
        <div class="header__container">
            <router-link to="/" class="header__logo">
                Padarunak.by
            </router-link>
            <ul class="header__menu">
                <li>
                    <router-link to="/about">О нас</router-link>
                </li>
                <li>
                    <router-link to="/pricing">Прайс</router-link>
                </li>
                <li>
                    <router-link to="/contact">Контакты</router-link>
                </li>
            </ul>
            <router-link to="/" class="header__lk">Войти</router-link>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'PageHeader',
    }
</script>