from django.contrib import admin

from .models import InternetIdentity, User

admin.site.register(User)
admin.site.register(InternetIdentity)
