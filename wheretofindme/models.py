from collections import defaultdict
from urllib.parse import urlparse

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

ICONS = defaultdict(lambda: "fas fa-link", {
    "facebook.com": "fab fa-facebook",
    "www.facebook.com": "fab fa-facebook",

    "github.com": "fab fa-github",
    "www.github.com": "fab fa-github",

    "instagram.com": "fab fa-instagram",
    "www.instagram.com": "fab fa-instagram",

    "keybase.io": "fab fa-keybase",

    "mastodon.social": "fab fa-mastodon",

    "plus.google.com": "fab fa-google-plus-g",

    "twitch.tv": "fab fa-twitch",
    "www.twitch.tv": "fab fa-twitch",

    "twitter.com": "fab fa-twitter",
    "www.twitter.com": "fab fa-twitter",

    "youtube.com": "fab fa-youtube",
    "www.youtube.com": "fab fa-youtube",
})

TYPES = defaultdict(lambda: "link", {
    "facebook.com": "Facebook",
    "www.facebook.com": "Facebook",

    "github.com": "GitHub",
    "www.github.com": "GitHub",

    "instagram.com": "Instagram",
    "www.instagram.com": "Instagram",

    "keybase.io": "Keybase",

    "mastodon.social": "Mastodon",

    "plus.google.com": "G+",

    "twitch.tv": "Twitch",
    "www.twitch.tv": "Twitch",

    "twitter.com": "Twitter",
    "www.twitter.com": "Twitter",

    "youtube.com": "YouTube",
    "www.youtube.com": "YouTube",
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

    def type_name(self):
        if self.url.startswith("mailto:"):
            return "Email"
        netloc = urlparse(self.url).netloc
        return TYPES[netloc]
