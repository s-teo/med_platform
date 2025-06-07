from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    ProfileUpdateSerializer,
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.cache import cache
import random

from .models import User
from .utils.twilio import send_sms_code  # импорт функции для отправки SMS


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 📱 1. Отправка кода на телефон с интеграцией Twilio
class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    # def post(self, request):
    #     phone = request.data.get("phone")
    #     if not phone:
    #         return Response({"error": "Телефон обязателен"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     code = str(random.randint(1000, 9999))
    #     cache.set(f'verify_code_{phone}', code, timeout=300)  # код действует 5 минут
    #
    #     try:
    #         send_sms_code(phone, code)
    #     except Exception as e:
    #         return Response({"error": f"Ошибка отправки SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #     return Response({"message": "Код отправлен"})
    def post(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"error": "Телефон обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        code = str(random.randint(1000, 9999))
        cache.set(f'verify_code_{phone}', code, timeout=300)  # 5 минут

        # Здесь можно подключить реальное SMS API
        print(f"[DEBUG] Отправка кода на {phone}: {code}")

        return Response({"message": "Код отправлен"})

# ✅ 2. Подтверждение кода
class VerifyPhoneCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")

        if not phone or not code:
            return Response({"error": "Телефон и код обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        real_code = cache.get(f'verify_code_{phone}')
        if real_code == code:
            try:
                user = User.objects.get(phone=phone)
                user.is_phone_verified = True
                user.save()
            except User.DoesNotExist:
                return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

            cache.delete(f'verify_code_{phone}')
            return Response({"message": "Телефон подтверждён"})

        return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)


