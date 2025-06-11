import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        receiver_id = data.get("receiver_id")

        receiver = None
        if receiver_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            receiver = await database_sync_to_async(User.objects.get)(id=receiver_id)

        await database_sync_to_async(ChatMessage.objects.create)(
            room_name=self.room_name,
            user=self.scope["user"],
            receiver=receiver,  # <-- добавляем получателя
            message=message,
            timestamp=now(),
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.scope["user"].username,
                "receiver_id": receiver_id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))
