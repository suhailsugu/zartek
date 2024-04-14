
from rest_framework import serializers
from apps.rides.models import Rides


class AllRidesListingSchema(serializers.ModelSerializer):
    rider  = serializers.CharField(source='rider.username',allow_null=True)
    driver = serializers.CharField(source='driver.username',allow_null=True)
    
    class Meta:
        model = Rides
        fields = ['pk','rider', 'driver', 'pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude','status','created_at','updated_at']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas


