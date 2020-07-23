==============
Wheretofind.me
==============

.. image:: https://readthedocs.org/projects/where-to-find-me/badge/?version=latest
   :target: https://where-to-find-me.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Server development
------------------

You will need:

* Python 3.8 or later (``brew install python@3.8``)
* PostgreSQL (``brew install postgres`` or Postgres.app_)
* yarn (``brew install yarn``)
* virtualenv

.. _Postgres.app: https://postgresapp.com/

Ensure the development database exists::

   createdb wheretofindme

Set the following environment variables in a ``.env`` file in the repo
root::

   export DJANGO_SECRET_KEY=$(uuidgen)
   export DJANGO_DEBUG=True
   export SENDGRID_API_KEY=INVALID

Set up your virtualenv with your preferred method. For me, using
``virtualenvwrapper`` and ``pyenv``, this looks like::

   $ mkvirtualenv wheretofindme --python=$(pyenv which python3.8)
   $ setvirtualenvproject
   $ pip install pip-tools
   $ pip-sync requirements/dev.txt requirements/base.txt

Then get the database into a good state::

   $ python manage.py migrate

Then get the frontend building::

   $ yarn install
   $ yarn serve

Then, you can visit the local site at ``http://localhost:8000/``. The
terminal output will say ``:8080``, but ignore it, it's a liar.

Dependencies
------------

To add Python dependencies, add them to ``requirements/{dev,base}.in``,
then recompile the locks::

   $ pip-compile requirements/base.in
   $ pip-compile requirements/dev.in

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
