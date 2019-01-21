from collections import defaultdict
from urllib.parse import urlparse

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

ICONS = defaultdict(
    lambda: "fas fa-link",
    {
        "facebook.com": "fab fa-facebook",
        "www.facebook.com": "fab fa-facebook",
        "github.com": "fab fa-github",
        "www.github.com": "fab fa-github",
        "instagram.com": "fab fa-instagram",
        "www.instagram.com": "fab fa-instagram",
        "keybase.io": "fab fa-keybase",
        "www.keybase.io": "fab fa-keybase",
        "mastodon.social": "fab fa-mastodon",
        "plus.google.com": "fab fa-google-plus-g",
        "twitch.tv": "fab fa-twitch",
        "www.twitch.tv": "fab fa-twitch",
        "twitter.com": "fab fa-twitter",
        "www.twitter.com": "fab fa-twitter",
        "youtube.com": "fab fa-youtube",
        "www.youtube.com": "fab fa-youtube",
        "behance.net": "fab fa-behance",
        "www.behance.net": "fab fa-behance",
        "bitbucket.org": "fab fa-bitbucket",
        "www.bitbucket.org": "fab fa-bitbucket",
        "deviantart.com": "fab fa-deviantart",
        "www.deviantart.com": "fab fa-deviantart",
        "pluspora.com": "fab fa-diaspora",
        "www.pluspora.com": "fab fa-diaspora",
        "dribbble.com": "fab fa-dribbble",
        "www.dribbble.com": "fab fa-dribbble",
        "ello.co": "fab fa-ello",
        "www.ello.co": "fab fa-ello",
        "codepen.io": "fab fa-codepen",
        "www.codepen.io": "fab fa-codepen",
        "discordapp.com": "fab fa-discord",
        "www.discordapp.com": "fab fa-discord",
        "vimeo.com": "fab fa-vimeo",
        "www.vimeo.com": "fab fa-vimeo",
        "untappd.com": "fab fa-untappd",
        "www.untappd.com": "fab fa-untappd",
        "tumblr.com": "fab fa-tumblr",
        "www.tumblr.com": "fab fa-tumblr",
        "teamspeak.com": "fab fa-teamspeak",
        "www.teamspeak.com": "fab fa-teamspeak",
        "steamcommunity.com": "fab fa-steam",
        "www.steamcommunity.com": "fab fa-steam",
        "stackoverflow.com": "fab fa-stackoverflow",
        "www.stackoverflow.com": "fab fa-stackoverflow",
        "soundcloud.com": "fab fa-soundcloud",
        "www.soundcloud.com": "fab fa-soundcloud",
        "snapchat.com": "fab fa-snapchat",
        "www.snapchat.com": "fab fa-snapchat",
        "slack.com": "fab fa-slack",
        "www.slack.com": "fab fa-slack",
        "skype.com": "fab fa-skype",
        "www.skype.com": "fab fa-skype",
        "reddit.com": "fab fa-reddit",
        "www.reddit.com": "fab fa-reddit",
        "pinterest.com": "fab fa-pinterest",
        "www.pinterest.com": "fab fa-pinterest",
        "patreon.com": "fab fa-patreon",
        "www.patreon.com": "fab fa-patreon",
        "paypal.com": "fab fa-paypal",
        "www.paypal.com": "fab fa-paypal",
        "medium.com": "fab fa-medium",
        "www.medium.com": "fab fa-medium",
        "kickstarter.com": "fab fa-kickstarter",
        "www.kickstarter.com": "fab fa-kickstarter",
        "goodreads.com": "fab fa-goodreads",
        "www.goodreads.com": "fab fa-goodreads",
        "gitlab.com": "fab fa-gitlab",
        "www.gitlab.com": "fab fa-gitlab",
        "etsy.com": "fab fa-etsy",
        "www.etsy.com": "fab fa-etsy",
    },
)


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    objects = UserManager()

    def follows(self):
        return [f.to_user for f in self.follow_set.prefetch_related("to_user")]

    def first_three(self):
        return self.internetidentity_set.exclude(name="")[:3]

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"slug": self.username})

    def primary_alias(self):
        return self.alias_set.first()


class InternetIdentity(models.Model):
    class Meta:
        verbose_name_plural = "Internet Identities"
        ordering = ("seq", "created_at")
        unique_together = [("user", "seq")]

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
        ordering = ("to_user__username", "from_user__username")
        unique_together = (("from_user", "to_user"),)

    from_user = models.ForeignKey(User, on_delete=models.PROTECT)
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")


class Alias(models.Model):
    class Meta:
        verbose_name_plural = "Aliases"
        ordering = ("seq", "name")

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    seq = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name!r} for {self.user.username}"


@receiver(post_save, sender=User)
def ensure_alias(sender, instance, created, **kwargs):
    if not instance.primary_alias():
        instance.alias_set.create(name=instance.username, seq=0)
