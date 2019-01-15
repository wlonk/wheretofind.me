==============
Infrastructure
==============

This is a memorandum about what we run where.

The app runs a web process on Heroku. Sendgrid and Postgres are
provisioned as Heroku addons.

SSL is provided by Heroku automatically.

DNS nameservers are through Cloudflare, which allows DNS flattening to
enable us to serve the app at the apex domain.
