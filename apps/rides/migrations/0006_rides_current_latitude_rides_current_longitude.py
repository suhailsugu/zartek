# Generated by Django 4.0.6 on 2024-04-13 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0005_alter_rides_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rides',
            name='current_latitude',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Current Latitude'),
        ),
        migrations.AddField(
            model_name='rides',
            name='current_longitude',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Current Longitude'),
        ),
    ]