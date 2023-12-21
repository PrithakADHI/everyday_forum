from django.urls import path
from chat.consumers import MychatApp

websocket_urlpatterns =[

    path('chat/ws/wsc/',MychatApp.as_asgi())
]