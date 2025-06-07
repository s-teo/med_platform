from rest_framework import serializers
from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model




# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'username', 'email')

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'phone']
        extra_kwargs = {
            'username': {'required': True},
            # другие валидации, если нужны
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'password')

    def validate_phone(self, value):
        if value == '':
            return None
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Необходимо указать имя пользователя и пароль.')

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Неверное имя пользователя или пароль.')

        if not user.is_active:
            raise serializers.ValidationError('Аккаунт деактивирован.')

        # Проверяем пароль через authenticate
        user_auth = authenticate(username=username, password=password)
        if not user_auth:
            raise serializers.ValidationError('Неверное имя пользователя или пароль.')

        # Всё ок, вызываем оригинальный validate, чтобы получить токены
        data = super().validate(attrs)
        return data