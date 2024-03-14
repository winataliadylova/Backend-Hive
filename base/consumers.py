import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'public_room'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        # print("type: ", type(event['message']))
        notif = event['message']
        # print(notif)
        notif = json.loads(notif)
        notif = notif[0]
        # print("type: ", type(notif))
        # # print()
        # print(json.dumps(notif['fields']))
        # await self.send(text_data=json.dumps({ 'message': event['message'] }))
        await self.send(text_data=json.dumps({ 'message': notif }))