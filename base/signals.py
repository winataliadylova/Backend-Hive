from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from .serializers import NotificationSerializer
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