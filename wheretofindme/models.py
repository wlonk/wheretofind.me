from collections import defaultdict
from urllib.parse import urlparse

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

ICONS = defaultdict(lambda: "fas fa-link", {
    "keybase.io": "fab fa-keybase",
    "mastodon.social": "fab fa-mastodon",
    "twitter.com": "fab fa-twitter",
    "facebook.com": "fab fa-facebook",
    "plus.google.com": "fab fa-google-plus-g",
    "twitch.tv": "fab fa-twitch",
    "instagram.com": "fab fa-instagram",
    "youtube.com": "fab fa-youtube",
    "github.com": "fab fa-github",
})


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    objects = UserManager()


class InternetIdentity(models.Model):
    class Meta:
        verbose_name_plural = "Internet Identities"
        ordering = (
            "created_at",
        )

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.name} at {self.url}"

    def looks_like_link(self):
        try:
            URLValidator()(self.url)
            valid = True
        except ValidationError:
            valid = False
        return self.url.startswith("mailto:") or valid

    def icon(self):
        if self.url.startswith("mailto:"):
            return "fas fa-envelope"
        netloc = urlparse(self.url).netloc
        return ICONS[netloc]
