import factory
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wheretofindme.User"

    email = factory.Sequence("user_{}@example.com".format)
    username = factory.Sequence("user_{}".format)

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        obj.set_password("foobar")
        obj.save()


@register
class InternetIdentityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wheretofindme.InternetIdentity"

    user = factory.SubFactory(UserFactory)
    name = "Test"
    url = "https://example.com/"


@register
class AliasFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wheretofindme.Alias"

    user = factory.SubFactory(UserFactory)
    name = "Test"


@register
class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wheretofindme.Follow"

    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
    nickname = ""


@pytest.fixture
def client(user_factory):
    user = user_factory()
    client = APIClient()
    client.force_login(user)
    client.user = user
    return client


@pytest.fixture
def anon_client():
    return APIClient()
