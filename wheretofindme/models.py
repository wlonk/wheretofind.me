from collections import defaultdict
from urllib.parse import urlparse

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

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


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    objects = UserManager()

    def follows(self):
        return [f.to_user for f in self.follow_set.prefetch_related("to_user")]

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"slug": self.username})


class InternetIdentity(models.Model):
    class Meta:
        verbose_name_plural = "Internet Identities"
        ordering = (
            "seq",
            "created_at",
        )
        unique_together = [
            ("user", "seq"),
        ]

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)
    seq = models.IntegerField(null=True)

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


class Follow(models.Model):
    class Meta:
        ordering = (
            "to_user__username",
        )

    from_user = models.ForeignKey(User, on_delete=models.PROTECT)
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
