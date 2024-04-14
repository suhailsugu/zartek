from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    
    path('create-or-update-user', views.CreateOrUpdateUserApiView.as_view(), name='create-or-update-user'),
    path(r'get-users', views.GetUsersApiView.as_view()),
    
    path('update-driver-location', views.UpdateDriverLocationApiView.as_view()),
    
    path('pending-ride-request', views.PendingRequestForDriverView.as_view()),
    path('accept-ride-request', views.AcceptRideRequestApiView.as_view()),
    
]
