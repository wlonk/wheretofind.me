import Vue from 'vue';
import VueCookie from 'vue-cookie';
import axios from 'axios';
import VueAxios from 'vue-axios';
// To support dropdowns, etc.:
import 'bootstrap';
import './scss/main.scss';

import FavStar from './components/FavStar.vue';
import IdentitiesForm from './components/IdentitiesForm.vue';
import AliasForm from './components/AliasForm.vue';

const instance = axios.create({
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  baseURL: '/',
  withCredentials: true,
});

Vue.config.productionTip = false;
Vue.use(VueCookie);
Vue.use(VueAxios, instance);

Array.from(document.querySelectorAll('.favstar')).forEach(el => {
  const data = {
    active: el.dataset.active !== 'false',
    username: el.dataset.username,
    small: el.classList.contains('btn-sm'),
  };
  new Vue({
    el,
    render: createElement => createElement(FavStar, { props: data }),
  });
});

Array.from(document.querySelectorAll('#edit-identities-form')).forEach(el => {
  new Vue({
    el,
    render: createElement => createElement(IdentitiesForm),
  });
});

Array.from(document.querySelectorAll('#edit-aliases-form')).forEach(el => {
  new Vue({
    el,
    render: createElement => createElement(AliasForm),
  });
});
