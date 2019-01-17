import Vue from 'vue';
import VueCookie from 'vue-cookie';
import axios from 'axios';
import VueAxios from 'vue-axios';

import FavStar from './FavStar.vue';
import EditIdentitiesForm from './EditIdentitiesForm.vue';

const instance = axios.create({
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  baseURL: '/',
  withCredentials: true,
});

Vue.config.productionTip = false;
Vue.use(VueCookie);
Vue.use(VueAxios, instance);

Array.from(document.getElementsByClassName('favstar')).forEach(el => {
  const data = {
    active: el.dataset.active !== 'false',
    username: el.dataset.username,
  };
  new Vue({
    el,
    render: createElement => createElement(FavStar, { props: data }),
  });
});

new Vue({
  render: createElement => createElement(EditIdentitiesForm),
}).$mount('#edit-identities-form');
