# Generated by Django 4.0.6 on 2024-04-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0006_rides_current_latitude_rides_current_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='rides',
            name='driver_approved',
            field=models.BooleanField(default=False, verbose_name='Driver Approved'),
        ),
    ]
