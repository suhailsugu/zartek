import re
from rest_framework import serializers
from apps.users.models import DriverRideRequest, Users
from zartek.helpers.helper import get_object_or_none, get_token_user_or_none
from django.db.models import Q

from zartek.helpers.nearest_driver_find import DRIVER_LOCATE



class CreateOrUpdateUserSerializer(serializers.ModelSerializer):
    user        = serializers.IntegerField(required=False,allow_null=True)
    username    = serializers.CharField(required=True)
    email       = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    password    = serializers.CharField(required=False)
    is_admin    = serializers.BooleanField(default=False)
    is_staff    = serializers.BooleanField(default=False)
    user_type   = serializers.ChoiceField(choices=Users.UserTypeChoice.choices,required=False)
    
    class Meta:
        model = Users 
        fields = ['user','username','email','password','is_active','is_admin','is_staff','user_type']
    
    
    def validate(self, attrs):
        email           = attrs.get('email', '')
        user            = attrs.get('user', None)
        username        = attrs.get('username', None)
        password        = attrs.get('password', None)
        
        user_query_set = Users.objects.filter(email=email)

        if username is not None:
            if not re.match("^[a-zA-Z0-9._@]*$", username):
                raise serializers.ValidationError({'username':("Enter a valid Username. Only alphabets, numbers, '@', '_', and '.' are allowed.")})
            
        if user is not None:
            user_query_set = user_query_set.exclude(pk=user)
            
        if user_query_set.exists():
            raise serializers.ValidationError({"username":('Username already exists!')})
        
        if password is not None and (len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?\'\"\\/~`' for char in password)):
            raise serializers.ValidationError({"password":('Must Contain 8 Characters, One Uppercase, One Lowercase, One Number and One Special Character')})
            
            
        return super().validate(attrs)
  

    def create(self, validated_data):
        password                  = validated_data.get('password')
        
        instance                  = Users()
        instance.username         = validated_data.get('username')
        instance.email            = validated_data.get('email')
        instance.set_password(password) 
        instance.is_active        = validated_data.get('is_active')
        instance.is_admin         = validated_data.get('is_admin')
        instance.is_staff         = True
        instance.user_type        = validated_data.get('user_type')
        instance.save()
        
        return instance

    
    def update(self, instance, validated_data):
        
        password = validated_data.get('password','')
 
        instance.username = validated_data.get('username')
        instance.email     = validated_data.get('email')
        if password:
            instance.set_password(password) 
        instance.is_active        = validated_data.get('is_active')
        instance.is_admin         = validated_data.get('is_admin')
        instance.is_staff         = True
        instance.user_type        = validated_data.get('user_type')
        instance.save()

                
        
        
        
        return instance


    
class UpdateDriverLocationSerializer(serializers.ModelSerializer):
    user              = serializers.IntegerField(required=False,allow_null=True)
    driver_latitude   = serializers.CharField(required=True)
    driver_longitude  = serializers.CharField(required=True)
  
    class Meta:
        model = Users 
        fields = ['user','driver_latitude','driver_longitude']
    
    
    def validate(self, attrs):
        return super().validate(attrs)

    
    def update(self, instance, validated_data):
        instance.driver_latitude    = validated_data.get('driver_latitude')
        instance.driver_longitude   = validated_data.get('driver_longitude')
        instance.save()
        return instance


class AcceptRideRequestSerializer(serializers.ModelSerializer):
    id                = serializers.IntegerField(required=False,allow_null=True)
    driver_response   = serializers.BooleanField(required=True)
  
    class Meta:
        model = DriverRideRequest 
        fields = ['id','driver_response']
    
    
    def validate(self, attrs):
        request         = self.context.get('request',None)
        id              = attrs.get('id')
        user_instance   = get_token_user_or_none(request)

        request_instance = get_object_or_none(DriverRideRequest,pk=id)

        if request_instance is None:
            raise serializers.ValidationError({"request_instance":"Please Provide a valid Request"})
        
        if request_instance.driver != user_instance:
            raise serializers.ValidationError({"User":"The request is not Assigned to this User"})
        
        if not request_instance.is_active and request_instance.is_accepted:
            raise serializers.ValidationError({"Active":"The request is not Active"})
        
        return super().validate(attrs)

    
    def update(self, instance, validated_data):
        request  = self.context.get('request',None)

        driver_response =  validated_data.get('driver_response',None)
        ride_instance   = instance.ride_details 
        
        if driver_response :
           instance.is_accepted    = True
           instance.is_active      = False
           instance.save()
           ride_instance.driver_approved = True
           ride_instance.save()
        else:
           instance.is_accepted    = False
           instance.is_active      = False
           instance.save()
           ride_instance.driver_approved = False
           ride_instance.save()
           
           pickup_latitude   = ride_instance.pickup_latitude
           pickup_longitude  = ride_instance.pickup_longitude
           
           user = get_token_user_or_none(request)
           driver = DRIVER_LOCATE(pickup_latitude,pickup_longitude,ride_instance,user).find_driver()
        
           instance.driver =driver
           instance.save()
           

        


        
        return instance  