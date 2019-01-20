import pytest


@pytest.mark.django_db
def test_MeRedirectView(client):
    response = client.get("/me/")
    assert response.url == f"/@{client.user.username}"


@pytest.mark.django_db
def test_UserProfileView(user_factory, client):
    user_factory(username="faithful")
    response = client.get("/@faithful")
    assert "Where to find".encode("utf-8") in response.content


@pytest.mark.django_db
def test_EditView(client):
    response = client.get("/edit/")
    assert "Where are you?".encode("utf-8") in response.content


@pytest.mark.django_db
def test_FollowsView(client):
    response = client.get("/follows/")
    assert "Where is everyone else?".encode("utf-8") in response.content


@pytest.mark.django_db
def test_FollowersView(client):
    response = client.get("/followers/")
    assert "Who knows where I am?".encode("utf-8") in response.content


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
            {"id": id1.id, "name": "Test", "url": "https://example.com/"}
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
