import pytest

from wheretofindme.admin import follow_count, follower_count, internetidentity_count


@pytest.mark.django_db
def test_internetidentity_count(user_factory, internet_identity_factory):
    user = user_factory()
    for _ in range(3):
        internet_identity_factory(user=user)

    assert internetidentity_count(user) == 3


@pytest.mark.django_db
def test_follow_count(user_factory, follow_factory):
    user = user_factory()
    for _ in range(3):
        follow_factory(from_user=user, to_user=user_factory())

    assert follow_count(user) == 3


@pytest.mark.django_db
def test_follower_count(user_factory, follow_factory):
    user = user_factory()
    for _ in range(3):
        follow_factory(from_user=user_factory(), to_user=user)

    assert follower_count(user) == 3
