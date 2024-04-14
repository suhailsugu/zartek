from rest_framework import serializers
from apps.rides.models import Rides
from zartek.helpers.helper import get_object_or_none
from zartek.helpers.nearest_driver_find import DRIVER_LOCATE



class CreateOrUpdateRidesSerializer(serializers.Serializer):
    id                = serializers.IntegerField(required=False,allow_null=True)
    rider             = serializers.IntegerField(required=True)
    pickup_latitude   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    pickup_longitude  = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    dropoff_latitude  = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    dropoff_longitude = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    status            = serializers.ChoiceField(choices=Rides.RideStatusChoice.choices, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model   = Rides
        fields = ['id','rider','pickup_latitude', 'pickup_longitude','dropoff_latitude','dropoff_longitude','status']

    def validate(self, attrs):
        return super().validate(attrs)
    

    def create(self, validated_data):
        pickup_latitude   = validated_data.get('pickup_latitude', None)
        pickup_longitude  = validated_data.get('pickup_longitude', None)
        
        instance                    = Rides()
        instance.rider_id           = validated_data.get('rider', None)
        instance.pickup_latitude    = pickup_latitude
        instance.pickup_longitude   = pickup_longitude
        instance.dropoff_latitude   = validated_data.get('dropoff_latitude', None)
        instance.dropoff_longitude  = validated_data.get('dropoff_longitude', None)
        instance.status             = validated_data.get('status', None)
        instance.save()

        driver = DRIVER_LOCATE(pickup_latitude,pickup_longitude,instance).find_driver()
        
        instance.driver =driver
        instance.save()
        
        return instance

    def update(self, instance, validated_data):
        pickup_latitude   = validated_data.get('pickup_latitude', None)
        pickup_longitude  = validated_data.get('pickup_longitude', None)
        
        instance.rider_id           = validated_data.get('rider', None)
        instance.pickup_latitude    = pickup_latitude
        instance.pickup_longitude   = pickup_longitude
        instance.dropoff_latitude   = validated_data.get('dropoff_latitude', None)
        instance.dropoff_longitude  = validated_data.get('dropoff_longitude', None)
        instance.status             = validated_data.get('status', None)
        instance.save()

        driver = DRIVER_LOCATE(pickup_latitude,pickup_longitude,instance).find_driver()
        instance.driver =driver
        instance.save()
        
        return instance
    

class UpdateRideRequestStatusSerializer(serializers.Serializer):
    id        = serializers.IntegerField(required=True,allow_null=True)
    status    = serializers.ChoiceField(choices=Rides.RideStatusChoice.choices, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model   = Rides
        fields = ['id','status']

    def validate(self, attrs):
        rides_id = attrs.get('id',None)
        rides_instance = get_object_or_none(Rides,pk=rides_id)
        if rides_instance is None:
            raise serializers.ValidationError({'ride':("Enter a valid Ride Instance")})
        
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.status  = validated_data.get('status', None)
        instance.save()
        return instance
    

class UpdateRideLocationSerializer(serializers.ModelSerializer):
    id                 = serializers.IntegerField(required=True,allow_null=True)
    current_latitude   = serializers.CharField(required=True)
    current_longitude  = serializers.CharField(required=True)
  
    class Meta:
        model = Rides 
        fields = ['id','current_latitude','current_longitude']
    
    
    def validate(self, attrs):
        ride_instance = get_object_or_none(Rides,pk=attrs.get('id',None))
        
        if ride_instance is None:
            raise serializers.ValidationError({'ride':("Enter a valid Ride Instance")})
        
        return super().validate(attrs)

    
    def update(self, instance, validated_data):
        instance.current_latitude    = validated_data.get('current_latitude')
        instance.current_longitude   = validated_data.get('current_longitude')
        instance.save()
        return instance
    