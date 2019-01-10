==============
Wheretofind.me
==============

You will need:

* Python 3.7 or later (``brew install python@3.7``)
* Pipenv (``brew install pipenv``)
* PostgreSQL (``brew install postgres`` or Postgres.app_)

.. _Postgres.app: https://postgresapp.com/

Ensure the development database exists::

   createdb wheretofindme

Set the following environment variables in a ``.env`` file in the repo
root::

   export DJANGO_SECRET_KEY=$(uuidgen)
   export DJANGO_DEBUG=True
   export SENDGRID_API_KEY=INVALID

Use ``pipenv``::

   $ pipenv sync
   $ pipenv run python manage.py migrate
   $ pipenv run python manage.py runserver
