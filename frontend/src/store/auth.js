import { defineStore } from 'pinia';
import axios from '../services/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),

  actions: {
    async login(email, password) {
      try {
        const response = await axios.post('/users/login/', { email, password });
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        return true;
      } catch (error) {
        console.error('Error al iniciar sesión', error);
        return false;
      }
    },

    logout() {
      this.token = '';
      localStorage.removeItem('token');
    }
  }
});
