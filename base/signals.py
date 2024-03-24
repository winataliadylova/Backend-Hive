from django.db.models.signals import post_save
from django.db import connection
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification, Chat
from .serializers import NotificationSerializer, ChatSerializer
from django.core import serializers
import json

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        data = serializers.serialize('json', [instance,])
        print("Print Data  ", json.loads(data))
        notif = json.loads(data)
        notif = notif[0]
        print("type: ", type(notif))
        print()
        print(json.dumps(notif['fields']))
        print()
        # print(notif[0])
        channel_layer = get_channel_layer()
        # print(instance)
        room_name = (notif['fields']['type'] + "_" + str(notif['fields']['user_id']))
        print("room_name: " + room_name)
        async_to_sync(channel_layer.group_send)(
            room_name,
            {
                "type": "send_notification",
                "message": serializers.serialize('json', [instance])
            }
        )

@receiver(post_save, sender=Chat)
def chat_created(sender, instance, created, **kwargs):
    if created:
        data = serializers.serialize('json', [instance,])
        chat = json.loads(data)
        chat = chat[0]
        chatRoomId = chat['fields']['chat_room_id']
        
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM public.chat_room WHERE id = %s', [chatRoomId])
        chat_room = dictfetchall(cursor)
        provider_id = chat_room[0].get('provider_id')
        customer_id = chat_room[0].get('customer_id')
        
        roomName="chat_"+ str(customer_id) + "_" + str(provider_id) 
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            roomName,
            {
                "type": "chatroom_message",
                "message": serializers.serialize('json', [instance]),
            }
        )
        
### Helper function
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]