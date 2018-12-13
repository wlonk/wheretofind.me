from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import InternetIdentity, User


class MeRedirectView(RedirectView):
    permanent = False
    pattern_name = "user-profile"

    def get_redirect_url(self, *args, **kwargs):
        kwargs["slug"] = self.request.user.username
        return super().get_redirect_url(*args, **kwargs)


class UserProfileView(DetailView):
    model = User
    slug_field = "username"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["identities"] = context["object"].internetidentity_set.all()
        return context


class IdentityCreateView(CreateView):
    success_url = "/s/me/"
    model = InternetIdentity
    fields = ("name", "url")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IdentityUpdateView(UpdateView):
    success_url = "/s/me/"
    model = InternetIdentity
    fields = ("name", "url")


class IdentityDeleteView(DeleteView):
    success_url = "/s/me/"
    model = InternetIdentity
    fields = ("name", "url")
