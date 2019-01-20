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
    password = factory.PostGenerationMethodCall("set_password", "foobar")


@register
class InternetIdentityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wheretofindme.InternetIdentity"

    user = factory.SubFactory(UserFactory)
    name = "Test"
    url = "https://example.com/"


@pytest.fixture
def client(user_factory):
    user = user_factory()
    client = APIClient()
    client.force_login(user)
    client.user = user
    return client
