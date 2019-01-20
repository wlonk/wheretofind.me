import pytest


@pytest.mark.django_db
class TestUser:
    def test_follows(self, user):
        assert user.follows() == []

    def test_first_three(self, user):
        assert not user.first_three()

    def test_get_absolute_url(self, user_factory):
        user = user_factory(username="magnificent")
        assert user.get_absolute_url() == "/@magnificent"


@pytest.mark.django_db
class TestInternetIdentity:
    def test_str(self, user_factory, internet_identity_factory):
        user = user_factory(username="merciful")
        identity = internet_identity_factory(
            user=user, name="quaint", url="https://example.com/notebook"
        )
        assert str(identity) == "merciful's quaint at https://example.com/notebook"

    def test_looks_like_link_valid(self, internet_identity_factory):
        identity = internet_identity_factory(url="https://example.com/")
        assert identity.looks_like_link()

    def test_looks_like_link_invalid(self, internet_identity_factory):
        identity = internet_identity_factory(url="example#1234")
        assert not identity.looks_like_link()

    def test_icon_mailto(self, internet_identity_factory):
        identity = internet_identity_factory(url="mailto:test@example.com")
        assert identity.icon() == "fas fa-envelope"

    def test_icon_url(self, internet_identity_factory):
        identity = internet_identity_factory(url="https://example.com/")
        assert identity.icon() == "fas fa-link"
