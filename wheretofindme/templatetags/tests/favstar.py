import pytest

from ..favstar import nickname


@pytest.mark.django_db
def test_nickname_shows_nickname(user_factory, follow_factory):
    user1 = user_factory()
    user2 = user_factory()
    follow_factory(from_user=user1, to_user=user2, nickname="fortunate")

    assert nickname({"user": user1}, user2) == "fortunate"
