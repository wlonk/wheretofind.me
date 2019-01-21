from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Alias, Follow, InternetIdentity, User
from .serializers import AliasSerializer, FollowSerializer, IdentitySerializer


class MeRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "user-profile"

    def get_redirect_url(self, *args, **kwargs):
        kwargs["slug"] = self.request.user.username
        return super().get_redirect_url(*args, **kwargs)


class UserProfileView(DetailView):
    model = User
    slug_field = "username"
    # We have to set this so it doesn't clobber the `user` context variable:
    context_object_name = "user_in_question"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["identities"] = context["object"].internetidentity_set.all()
        return context


class EditView(LoginRequiredMixin, TemplateView):
    template_name = "wheretofindme/edit_identities.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["identities"] = self.request.user.internetidentity_set.all()
        return context


class FollowsView(LoginRequiredMixin, ListView):
    model = Follow

    def get_queryset(self):
        return Follow.objects.filter(from_user=self.request.user)


class FollowersView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = "wheretofindme/follower_list.html"

    def get_queryset(self):
        return Follow.objects.filter(to_user=self.request.user)


# API Views


class ReorderMixin:
    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def reorder(self, request):
        ids = {id: seq for (seq, id) in enumerate(request.data)}

        self.get_queryset().update(seq=None)
        for obj in self.get_queryset():
            obj.seq = ids.get(obj.id)
            obj.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class FollowViewset(viewsets.ModelViewSet):
    model = Follow
    serializer_class = FollowSerializer
    lookup_field = "to_user__username"

    def get_queryset(self):
        return Follow.objects.filter(from_user=self.request.user)


class AliasViewset(ReorderMixin, viewsets.ModelViewSet):
    model = Alias
    serializer_class = AliasSerializer

    def get_queryset(self):
        return Alias.objects.filter(user=self.request.user)


class IdentityViewset(ReorderMixin, viewsets.ModelViewSet):
    serializer_class = IdentitySerializer
    model = InternetIdentity

    def get_queryset(self):
        return InternetIdentity.objects.filter(user=self.request.user)
