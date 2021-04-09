from channels.routing import ProtocolTypeRouter, URLRouter
from sockets.routing import websockets
application = ProtocolTypeRouter({
    "websocket": websockets,
})
