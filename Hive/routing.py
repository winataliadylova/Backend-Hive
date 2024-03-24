from django.urls import re_path
from base import consumers

websocket_urlpatterns = [
    re_path(r"ws/notify/(?P<room_name>\w+)/$", consumers.NotificationConsumer.as_asgi()),
]