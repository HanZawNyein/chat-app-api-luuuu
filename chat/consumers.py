import json

from channels.auth import login
from channels.db import database_sync_to_async
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatHistory


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chats_%s' % self.id

        # join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        now = timezone.now()
        # save the session (if the session backend does not access the db you can use `sync_to_async`)
        await database_sync_to_async(self.scope["session"].save)()

        # create new message obj
        chat_history = ChatHistory(sender=data['sender'], receiver=data['receiver'], category=data['category'],
                                   message=data['message'])

        await database_sync_to_async(chat_history.save)()

        # receive a message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'category': data['category'],
                'message': data['message'],
                'sender': data['sender'],
                'receiver': data['receiver'],
                'datetime': now.isoformat()
            }
        )

    # receive message from the room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))


