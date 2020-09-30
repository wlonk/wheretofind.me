from collections import defaultdict

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
        "pixelfed.social": "fa fa-pixelfed",
        "matrix.to": "fa fa-matrix-org",
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
        "stackoverflow.com": "fab fa-stack-overflow",
        "www.stackoverflow.com": "fab fa-stack-overflow",
        "soundcloud.com": "fab fa-soundcloud",
        "www.soundcloud.com": "fab fa-soundcloud",
        "snapchat.com": "fab fa-snapchat-ghost",
        "www.snapchat.com": "fab fa-snapchat-ghost",
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
        "telegram.dog": "fab fa-telegram-plane",
        "telegram.me": "fab fa-telegram-plane",
        "t.me": "fab fa-telegram-plane",
        "linkedin.com": "fab fa-linkedin",
        "www.linkedin.com": "fab fa-linkedin",
        "paypal.me": "fab fa-paypal",
        "www.paypal.me": "fab fa-paypal",
        "angel.co": "fab fa-angellist",
        "www.angel.co": "fab fa-angellist",
        "500px.com": "fab fa-500px",
        "www.500px.com": "fab fa-500px",
        "bandcamp.com": "fab fa-bandcamp",
        "blogspot.com": "fab fa-blogger-b",
        "blogger.com": "fab fa-blogger-b",
        "www.blogger.com": "fab fa-blogger-b",
        "dev.to": "fab fa-dev",
        "www.dev.to": "fab fa-dev",
        "figma.com": "fab fa-figma",
        "www.figma.com": "fab fa-figma",
        "flickr.com": "fab fa-flickr",
        "www.flickr.com": "fab fa-flickr",
        "foursquare.com": "fab fa-foursquare",
        "www.foursquare.com": "fab fa-foursquare",
        "news.ycombinator.com": "fab fa-hacker-news-square",
        "hackerrank.com": "fab fa-hackerrank",
        "www.hackerrank.com": "fab fa-hackerrank",
        "jsfiddle.net": "fab fa-jsfiddle",
        "www.jsfiddle.net": "fab fa-jsfiddle",
        "kaggle.com": "fab fa-kaggle",
        "www.kaggle.com": "fab fa-kaggle",
        "leanpub.com": "fab fa-leanpub",
        "www.leanpub.com": "fab fa-leanpub",
        "npmjs.com": "fab fa-npm",
        "www.npmjs.com": "fab fa-npm",
        "periscope.tv": "fab fa-periscope",
        "www.periscope.tv": "fab fa-periscope",
        "producthunt.com": "fab fa-product-hunt",
        "www.producthunt.com": "fab fa-product-hunt",
        "quora.com": "fab fa-quora",
        "www.quora.com": "fab fa-quora",
        "slideshare.net": "fab fa-slideshare",
        "www.slideshare.net": "fab fa-slideshare",
        "spotify.com": "fab fa-spotify",
        "open.spotify.com": "fab fa-spotify",
        "stackexchange.com": "fab fa-stack-exchange",
        "www.stackexchange.com": "fab fa-stack-exchange",
        "strava.com": "fab fa-strava",
        "www.strava.com": "fab fa-strava",
        "trello.com": "fab fa-trello",
        "www.trello.com": "fab fa-trello",
        "tripadvisor.com": "fab fa-tripadvisor",
        "www.tripadvisor.com": "fab fa-tripadvisor",
        "vk.com": "fab fa-vk",
        "www.vk.com": "fab fa-vk",
        "wikipedia.org": "fab fa-wikipedia-w",
        "en.wikipedia.org": "fab fa-wikipedia-w",
        "wordpress.com": "fab fa-wordpress-simple",
        "play.google.com": "fab fa-google-play",
        "drive.google.com": "fab fa-google-drive",
        "flipboard.com": "fab fa-flipboard",
        "www.flipboard.com": "fab fa-flipboard",
        "dailymotion.com": "fab fa-dailymotion",
        "www.dailymotion.com": "fab fa-dailymotion",
        "itch.io": "fab fa-itch-io",
        "unsplash.com": "fab fa-unsplash",
        "www.unsplash.com": "fab fa-unsplash",
        "tiktok.com": "fab fa-tiktok",
        "www.tiktok.com": "fab fa-tiktok",
        "speakerdeck.com": "fab fa-speakerdeck",
        "www.speakerdeck.com": "fab fa-speakerdeck",
        "fdroid.org": "fa fa-f-droid",
        "www.fdroid.org": "fa fa-f-droid",
        "f-droid.org": "fa fa-f-droid",
        "www.f-droid.org": "fa fa-f-droid",
        "gitea.com": "fa fa-gitea",
        "www.gitea.com": "fa fa-gitea",
        "codiepie.com": "fa fa-codiepie",
        "www.codiepie.com": "fa fa-codiepie",
        "hackaday.io": "fa fa-hackaday",
        "www.hackaday.io": "fa fa-hackaday",
        "hackaday.com": "fa fa-hackaday",
        "www.hackaday.com": "fa fa-hackaday",
        "hackster.io": "fa fa-hackster",
        "www.hackster.io": "fa fa-hackster",
        "hashnode.dev": "fa fa-hashnode",
        "hashnode.com": "fa fa-hashnode",
        "www.hashnode.com": "fa fa-hashnode",
        "liberapay.com": "fa fa-liberapay",
        "www.liberapay.com": "fa fa-liberapay",
        "mixcloud.com": "fa fa-mixcloud",
        "www.mixcloud.com": "fa fa-mixcloud",
    },
)

ICON_CHOICES = (
    ("fas fa-link", "fas fa-link"),  # web
    ("fas fa-envelope", "fas fa-envelope"),  # email
    ("fab fa-500px", "fab fa-500px"),  # 500px
    ("fab fa-angellist", "fab fa-angellist"),  # AngelList
    ("fab fa-bandcamp", "fab fa-bandcamp"),  # BandCamp
    ("fab fa-behance", "fab fa-behance"),  # Behance
    ("fab fa-bitbucket", "fab fa-bitbucket"),  # Bitbucket
    ("fab fa-blogger-b", "fab fa-blogger-b"),  # Blogger
    ("fab fa-codepen", "fab fa-codepen"),  # Codepen
    ("fa fa-codiepie", "fa fa-codiepie"),  # Codiepie
    ("fab fa-dailymotion", "fab fa-dailymotion"),  # DailyMotion
    ("fab fa-dev", "fab fa-dev"),  # DEV.to
    ("fab fa-deviantart", "fab fa-deviantart"),  # Deviantart
    ("fab fa-diaspora", "fab fa-diaspora"),  # Diaspora
    ("fab fa-discord", "fab fa-discord"),  # Discord
    ("fab fa-dribbble", "fab fa-dribbble"),  # Dribbble
    ("fab fa-ello", "fab fa-ello"),  # Ello
    ("fab fa-etsy", "fab fa-etsy"),  # Etsy
    ("fa fa-f-droid", "fa fa-f-droid"),  # F-droid
    ("fab fa-facebook", "fab fa-facebook"),  # Facebook
    ("fab fa-figma", "fab fa-figma"),  # Figma
    ("fab fa-flickr", "fab fa-flickr"),  # Flickr
    ("fab fa-flipboard", "fab fa-flipboard"),  # Flipboard
    ("fab fa-foursquare", "fab fa-foursquare"),  # Foursquare
    ("fa fa-gitea", "fa fa-gitea"),  # Gitea
    ("fab fa-github", "fab fa-github"),  # GitHub
    ("fab fa-gitlab", "fab fa-gitlab"),  # Gitlab
    ("fab fa-goodreads", "fab fa-goodreads"),  # Goodreads
    ("fab fa-google-drive", "fab fa-google-drive"),  # Google Drive
    ("fab fa-google-play", "fab fa-google-play"),  # Google Play
    ("fab fa-google-plus-g", "fab fa-google-plus-g"),  # Google Plus
    ("fa fa-hackaday", "fa fa-hackaday"),  # Hackaday
    ("fab fa-hacker-news-square", "fab fa-hacker-news-square"),  # HackerNews
    ("fab fa-hackerrank", "fab fa-hackerrank"),  # HackerRank
    ("fa fa-hackster", "fa fa-hackster"),  # Hackster
    ("fa fa-hashnode", "fa fa-hashnode"),  # Hashnode
    ("fab fa-instagram", "fab fa-instagram"),  # Instagram
    ("fab fa-itch-io", "fab fa-itch-io"),  # itch.io
    ("fab fa-jsfiddle", "fab fa-jsfiddle"),  # JSFiddle
    ("fab fa-kaggle", "fab fa-kaggle"),  # Kaggle
    ("fab fa-keybase", "fab fa-keybase"),  # Keybase
    ("fab fa-kickstarter", "fab fa-kickstarter"),  # Kickstarter
    ("fab fa-lastfm", "fab fa-lastfm"),  # Last
    ("fab fa-leanpub", "fab fa-leanpub"),  # Leanpub
    ("fa fa-liberapay", "fa fa-liberapay"),  # Liberapay
    ("fab fa-linkedin", "fab fa-linkedin"),  # LinkedIn
    ("fab fa-mastodon", "fab fa-mastodon"),  # Mastodon
    ("fa fa-matrix-org", "fa fa-matrix-org"),  # Matrix
    ("fab fa-medium", "fab fa-medium"),  # Medium
    ("fa fa-mixcloud", "fa fa-mixcloud"),  # Mixcloud
    ("fab fa-npm", "fab fa-npm"),  # NPM
    ("fab fa-patreon", "fab fa-patreon"),  # Patreon
    ("fab fa-paypal", "fab fa-paypal"),  # Paypal
    ("fab fa-periscope", "fab fa-periscope"),  # Periscope
    ("fab fa-pinterest", "fab fa-pinterest"),  # Pinterest
    ("fa fa-pixelfed", "fa fa-pixelfed"),  # Pixelfed
    ("fab fa-product-hunt", "fab fa-product-hunt"),  # Product Hunt
    ("fab fa-quora", "fab fa-quora"),  # Quora
    ("fab fa-ravelry", "fab fa-ravelry"),  # Ravelry
    ("fab fa-reddit", "fab fa-reddit"),  # Reddit
    ("fab fa-skype", "fab fa-skype"),  # Skype
    ("fab fa-slack", "fab fa-slack"),  # Slack
    ("fab fa-slideshare", "fab fa-slideshare"),  # SlideShare
    ("fab fa-snapchat-ghost", "fab fa-snapchat-ghost"),  # Snapchat
    ("fab fa-soundcloud", "fab fa-soundcloud"),  # Soundcloud
    ("fab fa-spotify", "fab fa-spotify"),  # Spotify
    ("fab fa-speakerdeck", "fab fa-speakerdeck"),  # Speaker Deck
    ("fab fa-stack-exchange", "fab fa-stack-exchange"),  # Stack Exchange
    ("fab fa-stack-overflow", "fab fa-stack-overflow"),  # Stackoverflow
    ("fab fa-steam", "fab fa-steam"),  # Steam
    ("fab fa-strava", "fab fa-strava"),  # Strava
    ("fab fa-teamspeak", "fab fa-teamspeak"),  # Teamspeak
    ("fab fa-telegram-plane", "fab fa-telegram-plane"),  # Telegram
    ("fab fa-tiktok", "fab fa-tiktok"),  # Tiktok
    ("fab fa-trello", "fab fa-trello"),  # Trello
    ("fab fa-tripadvisor", "fab fa-tripadvisor"),  # Trip Advisor
    ("fab fa-tumblr", "fab fa-tumblr"),  # Tumblr
    ("fab fa-twitch", "fab fa-twitch"),  # Twitch
    ("fab fa-twitter", "fab fa-twitter"),  # Twitter
    ("fab fa-unsplash", "fab fa-unsplash"),  # Unsplash
    ("fab fa-untappd", "fab fa-untappd"),  # Untappd
    ("fab fa-vimeo", "fab fa-vimeo"),  # Vimeo
    ("fab fa-vk", "fab fa-vk"),  # VK
    ("fab fa-wikipedia-w", "fab fa-wikipedia-w"),  # Wikipedia
    ("fab fa-wordpress-simple", "fab fa-wordpress-simple"),  # Wordpress
    ("fab fa-youtube", "fab fa-youtube"),  # YouTube
)

ICON_HUMAN_NAMES = {
    "link": "web",
    "envelope": "email",
    "500px": "500px",
    "angellist": "AngelList",
    "bandcamp": "BandCamp",
    "behance": "Behance",
    "bitbucket": "Bitbucket",
    "blogger-b": "Blogger",
    "codepen": "Codepen",
    "codiepie": "Codiepie",
    "dailymotion": "DailyMotion",
    "dev": "DEV.to",
    "deviantart": "Deviantart",
    "diaspora": "Diaspora",
    "discord": "Discord",
    "dribbble": "Dribbble",
    "ello": "Ello",
    "etsy": "Etsy",
    "f-droid": "F-droid",
    "facebook": "Facebook",
    "figma": "Figma",
    "flickr": "Flickr",
    "flipboard": "Flipboard",
    "foursquare": "Foursquare",
    "gitea": "Gitea",
    "github": "GitHub",
    "gitlab": "Gitlab",
    "goodreads": "Goodreads",
    "google-drive": "Google Drive",
    "google-play": "Google Play",
<<<<<<< HEAD
    "google-plus-g": "Google Plus",
    "hacker-news-square": "Hacker News",
=======
    "google-plus": "Google Plus",
    "hackaday": "Hackaday",
    "hacker-news": "Hacker News",
>>>>>>> 98b2862... add icon parse support for hackaday links
    "hackerrank": "HackerRank",
    "hackster": "Hackster",
    "hashnode": "Hashnode",
    "instagram": "Instagram",
    "itch-io": "itch.io",
    "jsfiddle": "JSFiddle",
    "kaggle": "Kaggle",
    "keybase": "Keybase",
    "kickstarter": "Kickstarter",
    "lastfm": "Last",
    "leanpub": "Leanpub",
    "liberapay": "Liberapay",
    "linkedin": "LinkedIn",
    "mastodon": "Mastodon",
    "matrix-org": "Matrix",
    "medium": "Medium",
    "mixcloud": "Mixcloud",
    "npm": "NPM",
    "patreon": "Patreon",
    "paypal": "Paypal",
    "periscope": "Periscope",
    "pinterest": "Pinterest",
    "pixelfed": "Pixelfed",
    "product-hunt": "Product Hunt",
    "quora": "Quora",
    "ravelry": "Ravelry",
    "reddit": "Reddit",
    "skype": "Skype",
    "slack": "Slack",
    "slideshare": "SlideShare",
    "snapchat-ghost": "Snapchat",
    "soundcloud": "Soundcloud",
    "spotify": "Spotify",
    "speakerdeck": "Speaker Deck",
    "stack-exchange": "Stack Exchange",
    "stack-overflow": "Stack Overflow",
    "steam": "Steam",
    "strava": "Strava",
    "teamspeak": "Teamspeak",
    "telegram-plane": "Telegram",
    "tiktok": "Tiktok",
    "trello": "Trello",
    "tripadvisor": "Trip Advisor",
    "tumblr": "Tumblr",
    "twitch": "Twitch",
    "twitter": "Twitter",
    "unsplash": "Unsplash",
    "untappd": "Untappd",
    "vimeo": "Vimeo",
    "vk": "VK",
    "wikipedia-w": "Wikipedia",
    "wordpress-simple": "Wordpress",
    "youtube": "YouTube",
}

QUALITY_CHOICES = ((0, "low"), (1, "mid"), (2, "high"))


class User(AbstractUser):
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
