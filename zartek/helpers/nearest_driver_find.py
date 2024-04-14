from math import radians, sin, cos, sqrt, atan2
from apps.users.models import DriverRideRequest, Users
from django.db.models import Q


class DRIVER_LOCATE():
    
    def __init__(self,pickup_latitude=None, pickup_longitude=None,ride=None,user=None):
        self.pickup_latitude   = pickup_latitude
        self.pickup_longitude  = pickup_longitude
        self.ride_instance     = ride
        self.user_instance     = user

    def distancecheck(self,lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = 6371 * c
        return distance
    
    def driver_request(self,user):
        instance                = DriverRideRequest()
        instance.ride_details   = self.ride_instance
        instance.driver         = user
        instance.save()
        
        return
        
    def find_driver(self):

        user_queryset = Users.objects.filter(Q(user_type='Driver')&Q(is_active=True))


        if self.user_instance is not None:
            user_queryset = user_queryset.exclude(pk=self.user_instance.pk)
        
            
        min_distance  = float('inf')
        nearest_user  = None

        for user in user_queryset:
            driver_lat    = float(user.driver_latitude) if user.driver_latitude not in ['',None] else None
            driver_long   = float(user.driver_longitude) if user.driver_longitude not in ['',None] else None

            if  None in [driver_lat,driver_long,self.pickup_latitude,self.pickup_longitude]:
                return

            distance = self.distancecheck(float(self.pickup_latitude), float(self.pickup_longitude), driver_lat, driver_long)

            if distance < min_distance:
                min_distance = distance
                nearest_user = user
        
        self.driver_request(user)

        return nearest_user
            

        
        ...
        