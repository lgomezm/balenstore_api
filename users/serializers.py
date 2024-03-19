from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self):
        self.validated_data["password"] = make_password(
            self.validated_data.get("password")
        )
        return super(UserSerializer, self).create(self.validated_data)
