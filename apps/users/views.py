import sys,os
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.users.models import DriverRideRequest, Users
from apps.users.schemas import GetUsersApiSerializers, PendingRequestForDriverSchema
from apps.users.serializers import AcceptRideRequestSerializer, CreateOrUpdateUserSerializer, UpdateDriverLocationSerializer
from zartek.helpers.helper import get_object_or_none, get_token_user_or_none
from zartek.helpers.pagination import RestPagination
from zartek.helpers.response import ResponseInfo
from zartek.helpers.custom_messages import _success,_record_not_found
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
import logging
from django.db.models import Q



logger = logging.getLogger(__name__)

class CreateOrUpdateUserApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateUserApiView, self).__init__(**kwargs)
        
    serializer_class = CreateOrUpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Users"])
    def post(self, request):
        try:
            user_instance = get_object_or_none(Users,pk=request.data.get('user',None))
           
            serializer = self.serializer_class(user_instance, data=request.data, context = {'request' : request})
            
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
    

class GetUsersApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetUsersApiView, self).__init__(**kwargs)
        
    queryset = Users.objects.all().exclude(is_superuser=1).order_by('-id')
    serializer_class = GetUsersApiSerializers
    permission_classes = (IsAuthenticated,)
    pagination_class = RestPagination
    filter_backends    = [filters.SearchFilter]
    search_fields      = ['username','email',]
    
    @swagger_auto_schema(pagination_class=RestPagination, tags=["Users"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class UpdateDriverLocationApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateDriverLocationApiView, self).__init__(**kwargs)
        
    serializer_class   = UpdateDriverLocationSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Users"])
    def post(self, request):
        try:

            user_instance = get_object_or_none(Users,pk=request.data.get('user',None))
           
            serializer = self.serializer_class(user_instance, data=request.data, context = {'request' : request})
            
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


class PendingRequestForDriverView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(PendingRequestForDriverView, self).__init__(**kwargs)

    serializer_class = PendingRequestForDriverSchema
    permission_classes  = (IsAuthenticated,)
    pagination_class    = RestPagination

    @swagger_auto_schema(tags=["Users"],pagination_class=RestPagination)
    def get(self, request):

        try:
            user_instance   = get_token_user_or_none(request)
            queryset        = DriverRideRequest.objects.filter(Q(driver=user_instance)&Q(is_accepted=False)&Q(is_active=True))

            if user_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:

            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AcceptRideRequestApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(AcceptRideRequestApiView, self).__init__(**kwargs)
        
    serializer_class   = AcceptRideRequestSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Users"])
    def post(self, request):
        try:

            request_instance = get_object_or_none(DriverRideRequest,pk=request.data.get('id',None))
           
            serializer = self.serializer_class(request_instance, data=request.data, context = {'request' : request})
            
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
