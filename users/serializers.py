from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmCode


class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
    email = serializers.EmailField()



class UserAuthSerializer(UserValidateSerializer):
    pass


class UserCreateSerializer(UserValidateSerializer):

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("User already exists")
        return username


class ConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmCode
        fields = ['code']