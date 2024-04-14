import json
from channels.generic.websocket import WebsocketConsumer
from zartek.helpers.helper import get_object_or_none
from apps.rides.models import Rides

class RideUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json    = json.loads(text_data)
        ride_id           = text_data_json['ride_id']
        current_latitude  = text_data_json['current_latitude']
        current_longitude = text_data_json['current_longitude']
        
        try:
            ride = get_object_or_none(Rides,pk=ride_id)
            ride.current_latitude  = current_latitude
            ride.current_longitude = current_longitude
            ride.save()
            
            self.send(text_data=json.dumps({'message': 'Ride location updated successfully'}))
        except Rides.DoesNotExist:
            self.send(text_data=json.dumps({'message': 'Ride not found'}))