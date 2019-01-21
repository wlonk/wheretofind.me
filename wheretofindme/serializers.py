from rest_framework import serializers

from .models import Alias, Follow, InternetIdentity, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("search_enabled",)


class FollowSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Follow
        fields = ("from_user", "to_user")


class IdentitySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InternetIdentity
        fields = ("id", "name", "url", "user")


class AliasSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Alias
        fields = ("id", "name", "user")
