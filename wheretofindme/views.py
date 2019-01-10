from django.db import transaction
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import InternetIdentity, User
from .serializers import IdentitySerializer


class MeRedirectView(RedirectView):
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


class EditView(TemplateView):
    template_name = "wheretofindme/edit_identities.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["identities"] = self.request.user.internetidentity_set.all()
        return context


class IdentityViewset(viewsets.ModelViewSet):
    serializer_class = IdentitySerializer
    model = InternetIdentity

    def get_queryset(self):
        return InternetIdentity.objects.filter(user=self.request.user)

    @action(detail=False, methods=['POST'], name='Reorder Identities')
    @transaction.atomic
    def reorder(self, request):
        ids = {id: seq for (seq, id) in enumerate(request.data)}

        self.get_queryset().update(seq=None)
        for identity in self.get_queryset():
            identity.seq = ids.get(identity.id)
            identity.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
