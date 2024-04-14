# Generated by Django 4.0.6 on 2024-04-13 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0006_rides_current_latitude_rides_current_longitude'),
        ('users', '0002_users_driver_latitude_users_driver_longitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverRideRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False, verbose_name='Is Accepted')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_driver', to=settings.AUTH_USER_MODEL)),
                ('ride_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_ride', to='rides.rides')),
            ],
            options={
                'verbose_name': 'Rides',
                'verbose_name_plural': 'Ride',
            },
        ),
    ]