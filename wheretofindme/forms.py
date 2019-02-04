from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django_registration import validators
from django_registration.forms import RegistrationFormUniqueEmail

from .models import User


class CustomRegistrationForm(RegistrationFormUniqueEmail):
    """
    Subclass of RegistrationFormUniqueEmail that adds:

      - Case-insensitive unique requirement for username.
      - TOS acceptance field
      - Additional help information to username field.
      - Crispy Forms Bootstrap4 layout.
    """

    class Meta(RegistrationFormUniqueEmail.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[User.USERNAME_FIELD].validators.append(
            validators.CaseInsensitiveUnique(
                User, User.USERNAME_FIELD, validators.DUPLICATE_USERNAME
            )
        )
        self.fields["username"].help_text += (
            " You cannot change this without intervention from an admin, so "
            "consider carefully."
        )
        self.helper = FormHelper()
        self.helper.form_action = "django_registration_register"
        self.helper.layout = Layout(
            PrependedText("username", "https://wheretofind.me/@"),
            Field("email"),
            Field("password1"),
            Field("password2"),
            Field("tos"),
            Submit("save", "Sign up", css_class="btn btn-primary"),
        )

    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_(u"I have read and agree to the <a href='/tos/'>Terms of Service</a>"),
        error_messages={"required": validators.TOS_REQUIRED},
    )


class CustomAuthenticationForm(AuthenticationForm):
    """
    Subclass of AuthenticationForm that overrides the clean method to allow login with
    either username or email. Both should be unique, per the restrictions on the
    CustomRegistrationForm form above.
    """

    def _get_user_from_email(self, email):
        return User.objects.filter(email=email).first()

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:  # Try again with email
                user_from_email = self._get_user_from_email(username)
                if user_from_email:
                    username = user_from_email.username
                    self.user_cache = authenticate(
                        self.request, username=username, password=password
                    )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
