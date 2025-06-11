import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from .middleware import logger
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"User in scope: {self.scope.get('user')} ({type(self.scope.get('user'))})")

        try:
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
        except Exception as e:
            import traceback
            logger.error(f"❌ Error in connect(): {e}")
            logger.error(traceback.format_exc())
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
            try:
                receiver = await database_sync_to_async(User.objects.get)(id=receiver_id)
            except User.DoesNotExist:
                await self.send(text_data=json.dumps({"error": "Receiver does not exist."}))
                return

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


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
            user_id = self.scope['user'].id

            # Формируем уникальное название группы для приватной переписки (оба user_id включены)
            ids = sorted([str(user_id), self.receiver_id])
            self.room_group_name = f'private_chat_{"_".join(ids)}'

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

        receiver = await database_sync_to_async(User.objects.get)(id=self.receiver_id)

        await database_sync_to_async(ChatMessage.objects.create)(
            room_name=self.room_group_name,
            user=self.scope["user"],
            receiver=receiver,
            message=message,
            timestamp=now(),
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.scope["user"].username,
                "sender_id": self.scope["user"].id,
                "receiver_id": int(self.receiver_id),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
        }))