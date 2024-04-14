from django.test import TestCase
from django.urls import reverse
from apps.users.models import Users
from rest_framework import status
from rest_framework.test import APIClient
from apps.rides.models import Rides

class CreateOrUpdateRideRequestApiViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_ride_request(self):
        url = reverse('create-or-update-ride-request')
        data = {
            'rider': 27, 
            'pickup_latitude': 'Your Pickup Latitude',
            'pickup_longitude': 'Your Pickup Longitude',
            'dropoff_latitude': 'Your Dropoff Latitude',
            'dropoff_longitude': 'Your Dropoff Longitude',
            'status': 'Started', 
        }
        user = Users.objects.filter(username='lauren').last()
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_ride_request(self):
        ride = Rides.objects.create(
            id=27, 
            pickup_latitude='Your Pickup Latitude',
            pickup_longitude='Your Pickup Longitude',
            dropoff_latitude='Your Dropoff Latitude',
            dropoff_longitude='Your Dropoff Longitude',
            status='Started' 
        )
        url = reverse('create-or-update-ride-request', kwargs={'pk': ride.pk})
        data = {
            'status': 'Completed' 
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)