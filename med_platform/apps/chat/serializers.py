from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'room_name', 'user', 'message', 'timestamp', 'receiver')
        read_only_fields = ('id', 'user', 'timestamp')
