import pytest


@pytest.mark.django_db
class TestUser:
    def test_follows(self, user):
        assert user.follows() == []

    def test_get_absolute_url(self, user_factory):
        user = user_factory(username="magnificent")
        assert user.get_absolute_url() == "/@magnificent"

    def test_primary_alias_missing(self, user_factory):
        user = user_factory(username="wanting")
        user.alias_set.all().delete()
        assert user.primary_alias() == "wanting"

    def test_primary_alias_blank(self, user_factory):
        user = user_factory(username="wanting")
        user.alias_set.update(name="")
        assert user.primary_alias() == "wanting"

    def test_nickname_by(self, user_factory, follow_factory):
        user1 = user_factory()
        user2 = user_factory()
        follow_factory(from_user=user1, to_user=user2, nickname="invention")

        assert user1.nickname_by(user2) == ""
        assert user2.nickname_by(user1) == "invention"

    def test_should_show_quality(self, user_factory, internet_identity_factory):
        user = user_factory()
        internet_identity_factory(user=user, quality=1)
        internet_identity_factory(user=user, quality=1)
        internet_identity_factory(user=user, quality=1)

        assert not user.should_show_quality()

        user = user_factory()
        internet_identity_factory(user=user, quality=1)
        internet_identity_factory(user=user, quality=2)
        internet_identity_factory(user=user, quality=1)

        assert user.should_show_quality()


@pytest.mark.django_db
class TestInternetIdentity:
    def test_str(self, user_factory, internet_identity_factory):
        user = user_factory(username="merciful")
        identity = internet_identity_factory(user=user, name="quaint", url="gnorp")
        assert str(identity) == "merciful's quaint at gnorp"

    def test_looks_like_link_valid(self, requests_mock, internet_identity_factory):
        url = "https://example.com/"
        requests_mock.get(url, text="<html></html>")
        identity = internet_identity_factory(url=url)
        assert identity.looks_like_link()

    def test_looks_like_link_invalid(self, internet_identity_factory):
        identity = internet_identity_factory(url="example#1234")
        assert not identity.looks_like_link()

    def test_quality_icon(self, internet_identity_factory):
        assert (
            internet_identity_factory(quality=0).quality_img()
            == "images/quality-low.svg"
        )
        assert (
            internet_identity_factory(quality=1).quality_img()
            == "images/quality-mid.svg"
        )
        assert (
            internet_identity_factory(quality=2).quality_img()
            == "images/quality-high.svg"
        )

    def test_icon_to_search(self, internet_identity_factory):
        assert internet_identity_factory(icon="fas fa-link").icon_to_search() == ""
        assert (
            internet_identity_factory(icon="fab fa-mastodon").icon_to_search()
            == "mastodon"
        )

    def test_should_validate(
        self, user_factory, internet_identity_factory, requests_mock
    ):
        user = user_factory()
        text = f"""
        <html>
        <body>
        <a href="https://wheretofind.me/@{user.username}" rel="me">me</a>
        </body>
        </html>
        """
        url = "http://example.com/id"
        requests_mock.get(url, text=text)
        identity = internet_identity_factory(url=url, user=user)
        assert identity.verified_at is not None


@pytest.mark.django_db
class TestAlias:
    def test_str(self, user_factory, alias_factory):
        user = user_factory(username="quixotic")
        alias = alias_factory(name="phobic", user=user)
        assert str(alias) == "'phobic' for quixotic"

    def test_signal(self, user_factory):
        user = user_factory(username="hallowed")
        assert user.alias_set.count() == 1
        assert user.alias_set.first().name == "hallowed"
