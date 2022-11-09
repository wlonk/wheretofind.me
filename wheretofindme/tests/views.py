import pytest
from bs4 import BeautifulSoup
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_MeRedirectView(client):
    response = client.get("/me/")
    assert response.url == f"/@{client.user.username}"


@pytest.mark.django_db
class TestUserProfileView:
    def test_basic_view(self, user_factory, client):
        user_factory(username="faithful")
        response = client.get("/@faithful")
        assert "Where to find".encode("utf-8") in response.content

    def test_tag_filter(self, user_factory, client, internet_identity_factory):
        user = user_factory(username="faithful")
        internet_identity_factory(user=user, tag="unwritten")
        internet_identity_factory(user=user)
        response = client.get("/@faithful?tag=unwritten")
        soup = BeautifulSoup(response.content, "html.parser")
        assert len(soup.find_all(class_="card")) == 1


@pytest.mark.django_db
def test_EditIdentityView(client):
    response = client.get("/locations/")
    assert "Where are you?".encode("utf-8") in response.content


@pytest.mark.django_db
def test_EditAliasView(client):
    response = client.get("/aliases/")
    assert "What do people call you?".encode("utf-8") in response.content


@pytest.mark.django_db
def test_FollowsView(client):
    response = client.get("/follows/")
    assert "Who do I follow?".encode("utf-8") in response.content


@pytest.mark.django_db
def test_FollowersView(client):
    response = client.get("/followers/")
    assert "Who follows me?".encode("utf-8") in response.content


@pytest.mark.django_db
class TestFriendByServiceView:
    def test_no_search(self, client):
        response = client.get("/by-service/", data={"q": ""})
        assert "Who's on the null service".encode("utf-8") in response.content

    def test_mastodon_search(self, client):
        response = client.get("/by-service/", data={"q": "mastodon"})
        assert "Who's on Mastodon".encode("utf-8") in response.content


@pytest.mark.django_db
class TestSearchView:
    def test_no_match(self, anon_client, user_factory):
        user_factory(username="wistful", search_enabled=True)
        response = anon_client.get("/search/", {"q": "boundless"})
        assert (
            "Sorry, we couldn't find anyone matching that search".encode("utf-8")
            in response.content
        )

    def test_match(self, anon_client, user_factory):
        user_factory(username="searchable", search_enabled=True)
        response = anon_client.get("/search/", {"q": "searchable"})
        assert "searchable".encode("utf-8") in response.content

    def test_search_self(self, user_factory):
        user = user_factory(username="searchable", search_enabled=True)
        client = APIClient()
        client.force_login(user)
        response = client.get("/search/", {"q": "searchable"})
        assert "searchable".encode("utf-8") in response.content

    def test_search_followed(self, anon_client, user_factory, follow_factory):
        user = user_factory(username="banana", search_enabled=True)
        followed = user_factory(username="searchable", search_enabled=False)
        follow_factory(from_user=user, to_user=followed, nickname="Alex Rodriguez")
        client = APIClient()
        client.force_login(user)
        response = client.get("/search/", {"q": "Rodriguez"})
        assert "searchable".encode("utf-8") in response.content

    def test_duplicate_aliases(self, user_factory, alias_factory):
        user = user_factory(username="searchable", search_enabled=True)
        alias_factory(user=user, name="Search Daly")
        alias_factory(user=user, name="Search Nolan")
        client = APIClient()
        client.force_login(user)
        response = client.get("/search/", {"q": "Search"})
        soup = BeautifulSoup(response.content, "html.parser")
        assert len(soup.find_all(class_="card")) == 1


@pytest.mark.django_db
def test_ProfileViewSet(client):
    response = client.get("/api/profile/")
    assert response.json() == {"search_enabled": False}


@pytest.mark.django_db
def test_AliasViewSet(client):
    response = client.get("/api/aliases/")
    assert response.json() == [
        {"id": client.user.alias_set.first().id, "name": client.user.primary_alias()}
    ]


@pytest.mark.django_db
def test_FollowersViewSet(client):
    response = client.get("/api/follows/")
    assert response.json() == []


@pytest.mark.django_db
class TestIdentityViewset:
    def test_get_queryset(self, client, user_factory, internet_identity_factory):
        other_user = user_factory()
        id1 = internet_identity_factory(user=client.user)
        internet_identity_factory(user=other_user)
        response = client.get("/api/identities/")
        assert response.json() == [
            {
                "id": id1.id,
                "name": "Test",
                "url": "non URL value",
                "tag": "",
                "quality": 2,
                "icon": "fas fa-link",
            }
        ]

    def test_reorder(self, client, internet_identity_factory):
        id1 = internet_identity_factory(user=client.user)
        id2 = internet_identity_factory(user=client.user)
        response = client.post(
            "/api/identities/reorder/", [id2.id, id1.id], format="json"
        )

        assert response.status_code == 204

        id1.refresh_from_db()
        id2.refresh_from_db()

        assert id2.seq == 0
        assert id1.seq == 1
