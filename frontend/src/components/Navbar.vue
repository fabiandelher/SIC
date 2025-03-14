<template>
  <v-app-bar app>
    <v-toolbar-title>Sistema de Cotizaciones</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="logout">Cerrar Sesión</v-btn>
  </v-app-bar>
</template>

<script setup>
import { useAuthStore } from '../store/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>
