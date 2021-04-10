import pytest

from wheretofindme.forms import CustomAuthenticationForm, CustomRegistrationForm


def test_CustomRegistrationForm():
    """
    Test that init sets appropriate attributes.
    """
    form = CustomRegistrationForm()
    assert hasattr(form, "helper")
    assert hasattr(form.helper, "layout")


@pytest.mark.django_db
class TestCustomAuthenticationForm:
    def test_auth_with_username(self, user_factory):
        user = user_factory(username="aromatic", email="expand@example.com")
        user.set_password("wink")
        user.save()
        form = CustomAuthenticationForm(
            data={"username": "aromatic", "password": "wink"}
        )
        assert form.is_valid()
        assert form.clean() == {"username": "aromatic", "password": "wink"}

    def test_auth_with_email(self, user_factory):
        user = user_factory(username="aromatic", email="expand@example.com")
        user.set_password("veil")
        user.save()
        form = CustomAuthenticationForm(
            data={"username": "expand@example.com", "password": "veil"}
        )
        assert form.is_valid()
        assert form.clean() == {"username": "expand@example.com", "password": "veil"}

    def test_bad_auth(self):
        form = CustomAuthenticationForm(data={"username": "border", "password": "stop"})
        assert not form.is_valid()
        with pytest.raises(Exception):
            form.clean()
