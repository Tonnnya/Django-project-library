import json

class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            if self.user.role == 1:
                self.group_name = 'librarian'