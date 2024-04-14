import sys,os
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.rides.models import  Rides
from zartek.helpers.helper import get_object_or_none
from zartek.helpers.pagination import RestPagination
from zartek.helpers.response import ResponseInfo
from zartek.helpers.custom_messages import _success,_record_not_found
from rest_framework.permissions import IsAuthenticated
from apps.rides.serializers import  CreateOrUpdateRidesSerializer, UpdateRideLocationSerializer,UpdateRideRequestStatusSerializer
from apps.rides.schemas import AllRidesListingSchema
import logging
from drf_yasg import openapi
from django.db.models import Q



logger = logging.getLogger(__name__)



class CreateOrUpdateRideRequestApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateRideRequestApiView, self).__init__(**kwargs)
    
    serializer_class          = CreateOrUpdateRidesSerializer
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Rides"])
    def post(self, request):
        try:
            
            rides_instance = get_object_or_none(Rides,pk=request.data.get('id',None))

            serializer = self.serializer_class(rides_instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
                
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetRideRequestListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetRideRequestListApiView, self).__init__(**kwargs)
    
    serializer_class    = AllRidesListingSchema
    permission_classes  = [IsAuthenticated]
    pagination_class    = RestPagination
  
    search        = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="The search value ", required=False)
  
    @swagger_auto_schema(tags=["Rides"], manual_parameters=[search], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            search_value    = request.GET.get('search', None)

            filter_set = Q()
            if search_value not in ['',None]:
                filter_set = Q(rider=search_value) | Q(driver=search_value)
     
            queryset    = Rides.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 




class GetRideRequestDetailApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetRideRequestDetailApiView, self).__init__(**kwargs)

    serializer_class = AllRidesListingSchema
    permission_classes  = (IsAuthenticated,)

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=True, description="Enter id")

    @swagger_auto_schema(tags=["Rides"], manual_parameters=[id])
    def get(self, request):

        try:
            rides_instance = get_object_or_none(Rides, pk=request.GET.get('id', None))

            if rides_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = self.serializer_class(rides_instance, context={'request': request}).data
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:

            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UpdateRideRequestStatusApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateRideRequestStatusApiView, self).__init__(**kwargs)
    
    serializer_class          = UpdateRideRequestStatusSerializer
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Rides"])
    def post(self, request):
        try:
            
            rides_instance = get_object_or_none(Rides,pk=request.data.get('id',None))

            serializer = self.serializer_class(rides_instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
                
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UpdateRideLocationApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateRideLocationApiView, self).__init__(**kwargs)
        
    serializer_class   = UpdateRideLocationSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Rides"])
    def post(self, request):
        try:
            ride_instance = get_object_or_none(Rides,pk=request.data.get('id',None))
           
            serializer = self.serializer_class(ride_instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        




