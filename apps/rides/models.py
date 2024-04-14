from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import Users

# Create your models here.


class Rides(models.Model):
    class RideStatusChoice(models.TextChoices):
        Started   = 'Started'
        Inprocess = 'Inprocess'
        Completed = 'Completed'
        Cancelled = 'Cancelled'

    rider             = models.ForeignKey(Users, related_name="riders_rider", on_delete=models.CASCADE, null=True, blank=True)
    driver            = models.ForeignKey(Users, related_name="riders_driver", on_delete=models.CASCADE, null=True, blank=True)
    pickup_latitude   = models.CharField(_('Pickup Latitude'), max_length=256, null=True, blank=True)
    pickup_longitude  = models.CharField(_('Pickup Longitude'), max_length=256, null=True, blank=True)
    dropoff_latitude  = models.CharField(_('Dropoff Latitude'), max_length=256, null=True, blank=True)
    dropoff_longitude = models.CharField(_('Dropoff Longitude'), max_length=256, null=True, blank=True)
    current_latitude  = models.CharField(_('Current Latitude'), max_length=256, null=True, blank=True)
    current_longitude = models.CharField(_('Current Longitude'), max_length=256, null=True, blank=True)
    status            = models.CharField(_('Status'), max_length=256,choices=RideStatusChoice.choices, null=True, blank=True)
    created_at        = models.DateTimeField(_('Created At'), auto_now_add=True, editable=False, blank=True, null=True)
    updated_at        = models.DateTimeField(_('Updated At'), auto_now=True, editable=False, blank=True, null=True)
    driver_approved   = models.BooleanField(_('Driver Approved'),default=False)

 
    class Meta      : 
        verbose_name = 'Rides'
        verbose_name_plural = "Ride"

    def __str__(self):
        return str(self.rider)
    