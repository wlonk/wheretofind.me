from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Case, Q, Value, When
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from .models import ICON_HUMAN_NAMES, Alias, Follow, InternetIdentity, User
from .serializers import (
    AliasSerializer,
    FollowSerializer,
    IdentitySerializer,
    ProfileSerializer,
)


class MeRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    pattern_name = "user-profile"

    def get_redirect_url(self, *args, **kwargs):
        kwargs["slug"] = self.request.user.username
        return super().get_redirect_url(*args, **kwargs)


class UserProfileView(DetailView):
    model = User
    slug_field = "username__iexact"
    # We have to set this so it doesn't clobber the `user` context variable:
    context_object_name = "user_in_question"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = context["object"].identities()
        if "tag" in self.request.GET:
            qs = qs.filter(tag=self.request.GET["tag"])
        context["identities"] = qs
        return context


class EditIdentityView(LoginRequiredMixin, TemplateView):
    template_name = "wheretofindme/edit_identities.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["identities"] = self.request.user.internetidentity_set.all()
        return context


class EditAliasView(LoginRequiredMixin, TemplateView):
    template_name = "wheretofindme/edit_aliases.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["aliases"] = self.request.user.alias_set.all()
        return context


class FollowsView(LoginRequiredMixin, ListView):
    model = Follow
    paginate_by = 50

    def get_queryset(self):
        return Follow.objects.filter(from_user=self.request.user)


class FollowersView(LoginRequiredMixin, ListView):
    model = Follow
    paginate_by = 50
    template_name = "wheretofindme/follower_list.html"

    def get_queryset(self):
        return Follow.objects.filter(to_user=self.request.user)


class SearchView(ListView):
    model = User
    template_name = "wheretofindme/search.html"

    def get_queryset(self):
        search = self.request.GET.get("q", "")
        filter = Q(alias__name__search=search, search_enabled=True)
        if self.request.user.is_authenticated:
            filter |= Q(
                followed__from_user=self.request.user, followed__nickname__search=search
            ) | Q(followed__from_user=self.request.user, alias__name__search=search)
        qs = (
            User.objects.prefetch_related("alias_set")
            .prefetch_related("followed")
            .filter(filter)
            .distinct()
        )
        return qs


class FriendsByService(LoginRequiredMixin, ListView):
    model = User
    template_name = "wheretofindme/friends_by_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("q", "")
        if search:
            service_name = ICON_HUMAN_NAMES.get(search, search)
            is_a_fediverse = search in ("mastodon", "diaspora", "pixelfed", "peertube", "pleroma")
        else:
            service_name = "the null service"
            is_a_fediverse = False
        context["service_name"] = service_name
        context["is_a_fediverse"] = is_a_fediverse
        return context

    def get_queryset(self):
        search = self.request.GET.get("q", "")
        if not search:
            return User.objects.none()
        qs = User.objects.filter(
            followed__from_user=self.request.user,
            # This is a dumb hack to get the right type for an Identity:
            internetidentity__icon=f"fab fa-{search}",
        ).distinct()
        return qs


# API Views


class ReorderMixin:
    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def reorder(self, request):
        whens = [When(id=id, then=Value(seq)) for seq, id in enumerate(request.data)]
        self.get_queryset().update(seq=None)
        self.get_queryset().update(seq=Case(*whens, default=None))

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ProfileView(RetrieveUpdateAPIView):
    model = User
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


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
