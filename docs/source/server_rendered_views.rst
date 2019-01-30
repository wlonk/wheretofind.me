=====================
Server-rendered views
=====================

These are simple server-rendered Django views.

Accounts
--------

This mostly comes from ``django-registration`` and Django itself.

@<username>
-----------

This displays a basic user profile. Of note: we set the
``context_object_name`` attribute, because failing to do so would cause
a collision between the template variable for the requesting user, and
the template variable for the user being displayed.

Me
--

This just redirects to the profile page for the requesting user.

Search
------

This accepts one query string variable: ``q``. The view creates a
``tsvector`` and ``tsquery`` to do a full-text search on all the aliases
of *only the users who opt in to search*.

Locations
---------

This is the edit page for a user's list of ``InternetIdentity`` objects.
This is awkward! We refer to them as "locations" in the frontend, for
the most part, but the model is called ``InternetIdentity``. Welp.

Aliases
-------

This is the edit page for a user's list of Aliases, and where they can
set their search opt-in.

Follows
-------

This is the list of users the user follows, or favstar'd. This needs
better terminology.

Followers
---------

This is the list of users who follow the user, or favstar'd them. This
needs better terminology.

Static pages
------------

Terms of Service, About, and the root page are all simple
``TemplateView`` views.
