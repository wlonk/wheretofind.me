from django_registration.forms import RegistrationFormTermsOfService

from .models import User


class CustomUserForm(RegistrationFormTermsOfService):
    class Meta(RegistrationFormTermsOfService.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
