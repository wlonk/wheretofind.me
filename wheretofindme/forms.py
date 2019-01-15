from django import forms
from django.utils.translation import gettext_lazy as _

from django_registration import validators
from django_registration.forms import RegistrationFormUniqueEmail

from crispy_forms.bootstrap import PrependedText, Alert
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import User


class CustomUserForm(RegistrationFormUniqueEmail):
    class Meta(RegistrationFormUniqueEmail.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text += (
            " You cannot change this without intervention from an admin, so "
            "consider carefully."
        )
        self.fields["tos"].label = (
            "I have read and agree to the <a href='/tos/'>Terms of Service</a>"
        )
        self.helper = FormHelper()
        self.helper.form_action = 'django_registration_register'
        self.helper.layout = Layout(
            PrependedText("username", "https://wheretofind.me/@"),
            Field("email"),
            Field("password1"),
            Field("password2"),
            Field("tos"),
            Submit('save', 'Sign up', css_class="btn btn-primary"),
        )

    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_(u'I have read and agree to the Terms of Service'),
        error_messages={
            'required': validators.TOS_REQUIRED,
        }
    )
