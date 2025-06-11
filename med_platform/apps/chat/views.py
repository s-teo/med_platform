from rest_framework import generics
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework import permissions
from django.db.models import Q

class ChatMessageListAPIView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')


class ChatMessageCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PrivateChatMessageListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        other_user_id = self.kwargs['user_id']
        user = self.request.user
        return ChatMessage.objects.filter(
            (Q(user=user) & Q(receiver_id=other_user_id)) |
            (Q(user_id=other_user_id) & Q(receiver=user))
        ).order_by('timestamp')