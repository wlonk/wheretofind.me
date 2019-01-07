from rest_framework import serializers

from .models import InternetIdentity


class IdentitySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InternetIdentity
        fields = (
            "id",
            "name",
            "url",
            "user",
        )
