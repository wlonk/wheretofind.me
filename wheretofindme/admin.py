from django.contrib import admin

from .models import Alias, Follow, InternetIdentity, User

admin.site.register(InternetIdentity)
admin.site.register(Alias)
admin.site.register(Follow)


def internetidentity_count(obj):
    return obj.internetidentity_set.count()


internetidentity_count.short_description = "Number of Identities"


def follow_count(obj):
    return obj.follow_set.count()


follow_count.short_description = "Number of Follows"


def follower_count(obj):
    return Follow.objects.filter(to_user=obj).count()


follower_count.short_description = "Number of Followers"


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_active",
        "search_enabled",
        internetidentity_count,
        follow_count,
        follower_count,
    )


admin.site.register(User, UserAdmin)
