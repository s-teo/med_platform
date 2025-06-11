from rest_framework import serializers
from .models import ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()


class UserNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone']

class ReceiverNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone']

class ChatMessageSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    receiver = ReceiverNestedSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'receiver', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user', 'receiver']  # ← добавь 'receiver' сюда
