from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.serializers import ModelSerializer
from . import models


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta(ModelSerializer.Meta):
        model = models.User
        read_only_fields = [*ModelSerializer.Meta.read_only_fields, 'last_login', 'role']
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        auth_credentials = super().validate(attrs)

        return {
            "auth_credentials": auth_credentials,
            "user": UserSerializer(self.user).data
        }
