import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Order

class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            if self.user.role == 1:
                self.group_name = 'librarians'
            else:
                self.group_name = f'user_{self.user.id}'

            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def order_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'order_notification',
            'message': event['message'],
            'order_id': event['order_id'],
        }))
