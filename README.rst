==============
Wheretofind.me
==============

.. image:: https://badge.waffle.io/wlonk/wheretofind.me.svg?columns=all
   :target: https://waffle.io/wlonk/wheretofind.me
   :alt: 'Waffle.io - Columns and their card count'

.. image:: https://readthedocs.org/projects/where-to-find-me/badge/?version=latest
   :target: https://where-to-find-me.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

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

Tests
-----

The Python tests are written using ``pytest``, ``pytest-django``,
``pytest-cov``, and ``pytest-factoryboy``. You can run them easily with
``yarn py:test:unit``.

The JavaScript tests are written using Jest and Vue's unit-test helpers.
You can run them easily with ``yarn js:test:unit``.

We require 100% test coverage on both parts. We will gladly help you
with any test-writing issues you may have.
