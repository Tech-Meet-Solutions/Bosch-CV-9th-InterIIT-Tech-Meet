from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import SocketConsumer
websockets = URLRouter([
    path(
        "ws/<int:game_id>", SocketConsumer, name="socket-consumer",
    ),
])