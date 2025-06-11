from rest_framework import generics, permissions
from django.db.models import Q
from .serializers import ChatMessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import ChatMessage
from apps.doctors.models import Doctor  # Импорт модели Doctor


User = get_user_model()

class ChatListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs['receiver_id']
        return ChatMessage.objects.filter(
            Q(user=user, receiver_id=receiver_id) |  # исходящие
            Q(user_id=receiver_id, receiver=user)    # входящие
        ).order_by('timestamp')  # можно добавить сортировку по времени

class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.kwargs['receiver_id']
        serializer.save(user=self.request.user, receiver_id=receiver_id)


class DialogsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        messages = ChatMessage.objects.filter(Q(user=user) | Q(receiver=user))

        interlocutor_ids = set()
        for msg in messages:
            if msg.user == user and msg.receiver:
                interlocutor_ids.add(msg.receiver.id)
            elif msg.receiver == user and msg.user:
                interlocutor_ids.add(msg.user.id)

        dialogs = []
        for interlocutor_id in interlocutor_ids:
            last_msg = messages.filter(
                Q(user=user, receiver_id=interlocutor_id) |
                Q(user_id=interlocutor_id, receiver=user)
            ).order_by('-timestamp').first()

            interlocutor = User.objects.get(id=interlocutor_id)

            # Пытаемся найти врача, связанного с этим пользователем
            try:
                doctor = Doctor.objects.get(user=interlocutor)
                full_name = interlocutor.get_full_name() or interlocutor.username
                doctor_image = request.build_absolute_uri(doctor.doctor_image.url) if doctor.doctor_image else None
            except Doctor.DoesNotExist:
                full_name = interlocutor.get_full_name() or interlocutor.username
                doctor_image = None

            dialogs.append({
                "user_id": interlocutor.id,
                "username": interlocutor.username,
                "full_name": full_name,
                "doctor_image": doctor_image,
                "last_message": last_msg.message if last_msg else "",
                "timestamp": last_msg.timestamp if last_msg else None,
            })

        dialogs = sorted(dialogs, key=lambda x: x['timestamp'], reverse=True)
        return Response(dialogs)