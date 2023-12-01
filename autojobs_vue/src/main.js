import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faAngleDown, faPen, faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';

library.add(faPen, faPlus,faTrash, faAngleDown);

axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).component('font-awesome-icon', FontAwesomeIcon).use(store).use(router).mount('#app');
