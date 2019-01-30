========
REST API
========

The REST API is a pretty straightforward Django REST Framework API.

The ``identities``, ``follows``, and ``aliases`` endpoints are all
straightforward. Each only lets you create the relevant objects with
yourself as the ``user`` or ``from_user``, as appropriate.

The ``profile`` endpoint is a bit weirder. It is doesn't play with the
usual collection/instance pattern of other REST endpoints, because any
given user can only see and only edit just one profile: theirs. Of note,
it doesn't show up in the root API JSON object because I jammed it in to
the router by hand.

Reorder Mixin
-------------

The ``identities`` and ``aliases`` endpoints allow their objects to be
reordered. This happens through the ``ReorderMixin``, which adds a
``.../reorder/`` endpoint which expects a list of IDs in the desired
order. We hit the database twice, once to null out the existing ``seq``
values, and again with an absurd built ``Case`` statement that sets the
``seq`` values appropriately.
