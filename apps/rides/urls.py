
from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [

    re_path(r'^v1/', include([
        re_path(r'^riderequest/', include([
            path('create-or-update-ride-request',views.CreateOrUpdateRideRequestApiView.as_view(),name='create-or-update-ride-request'),
            path('get-ride-request-list', views.GetRideRequestListApiView.as_view()),
            path('get-ride-request-details', views.GetRideRequestDetailApiView.as_view()),
            path('update-ride-request-status',views.UpdateRideRequestStatusApiView.as_view()),
            path('update-ride-location', views.UpdateRideLocationApiView.as_view()),

        ]))
    ]))
]

