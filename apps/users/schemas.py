from rest_framework import serializers
from apps.users.models import DriverRideRequest, Users


class GetUsersApiSerializers(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['pk','username','email']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

    
class PendingRequestForDriverSchema(serializers.ModelSerializer):
    rider             = serializers.CharField(source='ride_details.rider.username',allow_null=True)
    pickup_latitude   = serializers.CharField(source='ride_details.pickup_latitude',allow_null=True)
    pickup_longitude  = serializers.CharField(source='ride_details.pickup_longitude',allow_null=True)
    dropoff_latitude  = serializers.CharField(source='ride_details.dropoff_latitude',allow_null=True)
    dropoff_longitude = serializers.CharField(source='ride_details.dropoff_longitude',allow_null=True)
    
    class Meta:
        model = DriverRideRequest
        fields = ['pk','rider', 'driver', 'pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
