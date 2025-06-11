from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'receiver', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user', 'receiver']  # ← добавь 'receiver' сюда
