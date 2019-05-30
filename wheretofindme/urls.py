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
from django.contrib.auth.views import LoginView
from django.urls import include, path
from django.views.generic.base import TemplateView
from django_registration.backends.activation.views import RegistrationView
from rest_framework import routers

from . import views
from .forms import CustomAuthenticationForm, CustomRegistrationForm

router = routers.DefaultRouter()
router.register("identities", views.IdentityViewset, basename="identity")
router.register("follows", views.FollowViewset, basename="follow")
router.register("aliases", views.AliasViewset, basename="alias")
router_urls = router.urls + [
    path("profile/", views.ProfileView.as_view(), name="profile")
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        LoginView.as_view(authentication_form=CustomAuthenticationForm),
        name="login",
    ),
    path(
        "accounts/register/",
        RegistrationView.as_view(form_class=CustomRegistrationForm),
        name="django_registration_register",
    ),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include((router_urls, "api"), namespace="api")),
    path("@<str:slug>", views.UserProfileView.as_view(), name="user-profile"),
    path("me/", views.MeRedirectView.as_view(), name="me"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("locations/", views.EditIdentityView.as_view(), name="identity-edit"),
    path("aliases/", views.EditAliasView.as_view(), name="alias-edit"),
    path("follows/", views.FollowsView.as_view(), name="follows"),
    path("followers/", views.FollowersView.as_view(), name="followers"),
    path("by-service/", views.FriendsByService.as_view(), name="by-service"),
    path("tos/", TemplateView.as_view(template_name="tos.html"), name="tos"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("", TemplateView.as_view(template_name="base.html"), name="root"),
]
