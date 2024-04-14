from django.urls import path
from apps.rides.realtime import RideUpdateConsumer

websocket_urlpatterns = [
    path('ws/ride_updates/', RideUpdateConsumer),
]