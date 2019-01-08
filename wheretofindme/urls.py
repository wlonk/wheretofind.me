"""wheretofindme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django_registration.backends.activation.views import RegistrationView
from rest_framework import routers

from . import views
from .forms import CustomUserForm

router = routers.DefaultRouter()
router.register(r"identities", views.IdentityViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/register/",
        RegistrationView.as_view(form_class=CustomUserForm),
        name="django_registration_register",
    ),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include(router.urls)),
    path("@<str:slug>/", views.UserProfileView.as_view(), name="user-profile"),
    path("s/me/", views.MeRedirectView.as_view(), name="me"),
    path("s/edit/", views.EditView.as_view(), name="identity-edit"),
    path("", TemplateView.as_view(template_name="base.html"), name="root"),
]
