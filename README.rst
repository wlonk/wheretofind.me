==============
Wheretofind.me
==============

.. image:: https://badge.waffle.io/wlonk/wheretofind.me.svg?columns=all
 :target: https://waffle.io/wlonk/wheretofind.me
 :alt: 'Waffle.io - Columns and their card count'

Server development
------------------

You will need:

* Python 3.7 or later (``brew install python@3.7``)
* Pipenv (``brew install pipenv``)
* PostgreSQL (``brew install postgres`` or Postgres.app_)
* yarn (``brew install yarn``)

.. _Postgres.app: https://postgresapp.com/

Ensure the development database exists::

   createdb wheretofindme

Set the following environment variables in a ``.env`` file in the repo
root::

   export DJANGO_SECRET_KEY=$(uuidgen)
   export DJANGO_DEBUG=True
   export SENDGRID_API_KEY=INVALID

Use ``pipenv`` to get the database into a good state::

   $ pipenv sync
   $ pipenv run python manage.py migrate

Then get the frontend building::

   $ yarn install
   $ yarn serve

Dependencies
------------

To add Python dependencies::

   $ pipenv install (--dev) <dep name>

To add JavaScript dependencies::

   $ yarn add (--dev) <dep name>
