from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    objects = UserManager()


class InternetIdentity(models.Model):
    class Meta:
        verbose_name_plural = "Internet Identities"

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.user.username}'s {self.name} at {self.url}"
