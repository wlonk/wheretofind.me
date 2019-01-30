================
Client-Side Code
================

We use Vue for our interactive frontend components. However, we do not
have and do not want a SPA. So in ``src/main.js`` we search the page for
a few mount points: ``.favstar``, ``#edit-identities-form``, and
``#edit-aliases-form``. The server renders these approximately like the
Vue templates that will replace them (with some differences, like
marking fields as ``disabled``).

The Vue components handle calling the REST API endpoints to live-save
any changes you make.
