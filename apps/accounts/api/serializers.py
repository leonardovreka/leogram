from rest_framework import serializers
from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def validate_email(self, value):
        return value.lower()

class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.UUIDField()

class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()