import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'  // 🔹 Verifica esta línea
import vuetify from './plugins/vuetify'

console.log("🚀 Montando Vue App...");

const app = createApp(App)

app.use(router)
app.use(vuetify)

app.mount('#app')

console.log("✅ Vue App montada correctamente!");
