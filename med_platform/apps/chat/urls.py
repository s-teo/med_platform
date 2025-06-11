from django.urls import path
from .views import ChatMessageListAPIView, ChatMessageCreateAPIView, PrivateChatMessageListAPIView

urlpatterns = [
    path('<str:room_name>/', ChatMessageListAPIView.as_view(), name='chat-messages'),
    path('', ChatMessageCreateAPIView.as_view(), name='chat-create'),
    path('private/<int:user_id>/', PrivateChatMessageListAPIView.as_view(), name='private-chat'),
]
