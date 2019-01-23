from django.contrib import admin

from .models import Alias, Follow, InternetIdentity, User

admin.site.register(User)
admin.site.register(InternetIdentity)
admin.site.register(Alias)
admin.site.register(Follow)
