from django.urls import path
from .views import (
    ProfileUpdateView,
    UserRegisterView,
    CustomTokenObtainPairView,
    SendVerificationCodeView,
    VerifyPhoneCodeView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileUpdateView.as_view(), name='profile-update'),
    path("send-code/", SendVerificationCodeView.as_view(), name="send-code"),
    path("verify-code/", VerifyPhoneCodeView.as_view(), name="verify-code"),

]