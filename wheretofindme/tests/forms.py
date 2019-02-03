import pytest

from wheretofindme.forms import CustomAuthForm, CustomUserForm


def test_CustomUserForm():
    """
    Test that init sets appropriate attributes.
    """
    form = CustomUserForm()
    assert hasattr(form, "helper")
    assert hasattr(form.helper, "layout")


@pytest.mark.django_db
class TestCustomAuthForm:
    def test_auth_with_username(self, user_factory):
        user_factory(username="aromatic", email="expand@example.com", password="wink")
        form = CustomAuthForm(data={"username": "aromatic", "password": "wink"})
        assert form.is_valid()
        assert form.clean() == {"username": "aromatic", "password": "wink"}

    def test_auth_with_email(self, user_factory):
        user_factory(username="aromatic", email="expand@example.com", password="veil")
        form = CustomAuthForm(
            data={"username": "expand@example.com", "password": "veil"}
        )
        assert form.is_valid()
        assert form.clean() == {"username": "expand@example.com", "password": "veil"}

    def test_bad_auth(self):
        form = CustomAuthForm(data={"username": "border", "password": "stop"})
        assert not form.is_valid()
        with pytest.raises(Exception):
            form.clean()
