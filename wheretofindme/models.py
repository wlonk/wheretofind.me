from collections import defaultdict

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
        "ravelry.com": "fab fa-ravelry",
        "www.ravelry.com": "fab fa-ravelry",
        "last.fm": "fab fa-lastfm",
        "www.last.fm": "fab fa-lastfm",
    },
)

ICON_CHOICES = (
    ("fas fa-link", "fas fa-link"),  # web
    ("fas fa-envelope", "fas fa-envelope"),  # email
    ("fab fa-behance", "fab fa-behance"),  # Behance
    ("fab fa-bitbucket", "fab fa-bitbucket"),  # Bitbucket
    ("fab fa-codepen", "fab fa-codepen"),  # Codepen
    ("fab fa-deviantart", "fab fa-deviantart"),  # Deviantart
    ("fab fa-diaspora", "fab fa-diaspora"),  # Diaspora
    ("fab fa-discord", "fab fa-discord"),  # Discord
    ("fab fa-dribbble", "fab fa-dribbble"),  # Dribbble
    ("fab fa-ello", "fab fa-ello"),  # Ello
    ("fab fa-etsy", "fab fa-etsy"),  # Etsy
    ("fab fa-facebook", "fab fa-facebook"),  # Facebook
    ("fab fa-github", "fab fa-github"),  # GitHub
    ("fab fa-gitlab", "fab fa-gitlab"),  # Gitlab
    ("fab fa-goodreads", "fab fa-goodreads"),  # Goodreads
    ("fab fa-google-plus-g", "fab fa-google-plus-g"),  # Google Plus
    ("fab fa-instagram", "fab fa-instagram"),  # Instagram
    ("fab fa-keybase", "fab fa-keybase"),  # Keybase
    ("fab fa-kickstarter", "fab fa-kickstarter"),  # Kickstarter
    ("fab fa-lastfm", "fab fa-lastfm"),  # Last
    ("fab fa-mastodon", "fab fa-mastodon"),  # Mastodon
    ("fab fa-medium", "fab fa-medium"),  # Medium
    ("fab fa-patreon", "fab fa-patreon"),  # Patreon
    ("fab fa-paypal", "fab fa-paypal"),  # Paypal
    ("fab fa-pinterest", "fab fa-pinterest"),  # Pinterest
    ("fab fa-ravelry", "fab fa-ravelry"),  # Ravelry
    ("fab fa-reddit", "fab fa-reddit"),  # Reddit
    ("fab fa-skype", "fab fa-skype"),  # Skype
    ("fab fa-slack", "fab fa-slack"),  # Slack
    ("fab fa-snapchat", "fab fa-snapchat"),  # Snapchat
    ("fab fa-soundcloud", "fab fa-soundcloud"),  # Soundcloud
    ("fab fa-stackoverflow", "fab fa-stackoverflow"),  # Stackoverflow
    ("fab fa-steam", "fab fa-steam"),  # Steam
    ("fab fa-teamspeak", "fab fa-teamspeak"),  # Teamspeak
    ("fab fa-tumblr", "fab fa-tumblr"),  # Tumblr
    ("fab fa-twitch", "fab fa-twitch"),  # Twitch
    ("fab fa-twitter", "fab fa-twitter"),  # Twitter
    ("fab fa-untappd", "fab fa-untappd"),  # Untappd
    ("fab fa-vimeo", "fab fa-vimeo"),  # Vimeo
    ("fab fa-youtube", "fab fa-youtube"),  # YouTube
)

ICON_HUMAN_NAMES = {
    "link": "web",
    "envelope": "email",
    "behance": "Behance",
    "bitbucket": "Bitbucket",
    "codepen": "Codepen",
    "deviantart": "Deviantart",
    "diaspora": "Diaspora",
    "discord": "Discord",
    "dribbble": "Dribbble",
    "ello": "Ello",
    "etsy": "Etsy",
    "facebook": "Facebook",
    "github": "GitHub",
    "gitlab": "Gitlab",
    "goodreads": "Goodreads",
    "google-plus-g": "Google Plus",
    "instagram": "Instagram",
    "keybase": "Keybase",
    "kickstarter": "Kickstarter",
    "lastfm": "Last",
    "mastodon": "Mastodon",
    "medium": "Medium",
    "patreon": "Patreon",
    "paypal": "Paypal",
    "pinterest": "Pinterest",
    "ravelry": "Ravelry",
    "reddit": "Reddit",
    "skype": "Skype",
    "slack": "Slack",
    "snapchat": "Snapchat",
    "soundcloud": "Soundcloud",
    "stackoverflow": "Stackoverflow",
    "steam": "Steam",
    "teamspeak": "Teamspeak",
    "tumblr": "Tumblr",
    "twitch": "Twitch",
    "twitter": "Twitter",
    "untappd": "Untappd",
    "vimeo": "Vimeo",
    "youtube": "YouTube",
}

QUALITY_CHOICES = ((0, "low"), (1, "mid"), (2, "high"))


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    objects = UserManager()

    search_enabled = models.BooleanField(default=False)

    def follows(self):
        return [f.to_user for f in self.follower.prefetch_related("to_user")]

    def identities(self):
        return self.internetidentity_set.exclude(name="")

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"slug": self.username})

    def primary_alias(self):
        alias = self.alias_set.first()
        if alias and alias.name:
            return alias.name
        return self.username

    def other_aliases(self):
        return self.alias_set.values_list("name", flat=True)[1:]

    def nickname_by(self, other):
        try:
            return other.follower.get(to_user=self).nickname
        except Follow.DoesNotExist:
            return ""

    def should_show_quality(self):
        qualities = self.internetidentity_set.exclude(name="").values_list(
            "quality", flat=True
        )
        return not all(q == qualities[0] for q in qualities)


class InternetIdentity(models.Model):
    class Meta:
        verbose_name_plural = "Internet Identities"
        ordering = ("seq", "created_at")
        unique_together = [("user", "seq")]

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default="fas fa-link")
    quality = models.PositiveSmallIntegerField(choices=QUALITY_CHOICES, default=2)
    tag = models.CharField(max_length=50, blank=True)
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

    def quality_img(self):
        if self.quality == 0:
            return "images/quality-low.svg"
        if self.quality == 1:
            return "images/quality-mid.svg"
        if self.quality == 2:
            return "images/quality-high.svg"

    def icon_to_search(self):
        if self.icon.startswith("fab fa-"):
            _, search = self.icon.split("-", 1)
            return search
        return ""


class Follow(models.Model):
    class Meta:
        ordering = ("to_user__username", "from_user__username")
        unique_together = (("from_user", "to_user"),)

    from_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="follower"
    )
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="followed")
    nickname = models.CharField(max_length=128, blank=True)


class Alias(models.Model):
    class Meta:
        verbose_name_plural = "Aliases"
        ordering = ("seq", "name")

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=128, blank=True)
    seq = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name!r} for {self.user.username}"


@receiver(post_save, sender=User)
def ensure_alias(sender, instance, created, **kwargs):
    if not instance.alias_set.exists():
        instance.alias_set.create(name=instance.username, seq=0)
