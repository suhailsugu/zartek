from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _

# Create your models here.



class UserManager(BaseUserManager):
    def create_user(self, username, password = None, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))

        user = self.model(username = username, **extra_fields)
        if password:
            user.set_password(password.strip())
            
        user.save()
        return user


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_admin', True)
     
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        
        return self.create_user(username, password, **extra_fields)




class Users(AbstractBaseUser, PermissionsMixin):
    class UserTypeChoice(models.TextChoices):
        Rider   = 'Rider'
        Driver  = 'Driver'
    
    email               = models.EmailField(_('Email'), max_length = 255, unique = True, blank = True, null = True)
    username            = models.CharField(_('User Name'), max_length = 300, blank = True, null = True)
    is_verified         = models.BooleanField(default = False)
    is_admin            = models.BooleanField(default = False)
    is_active           = models.BooleanField(default = True)
    is_staff            = models.BooleanField(default = False)
    is_superuser        = models.BooleanField(default = False)
    user_type           = models.CharField(_('User Type'), max_length=100, choices=UserTypeChoice.choices, null=True,blank=True)
    driver_latitude     = models.CharField(_('Driver Latitude'), max_length=256, null=True, blank=True)
    driver_longitude    = models.CharField(_('Driver Longitude'), max_length=256, null=True, blank=True)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj = None):
        "Does the user have a specific permission?"
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True


class DriverRideRequest(models.Model):
    ride_details      = models.ForeignKey('rides.Rides', related_name="requested_ride", on_delete=models.CASCADE, null=True, blank=True)
    driver            = models.ForeignKey(Users, related_name="request_driver", on_delete=models.CASCADE, null=True, blank=True)
    is_accepted       = models.BooleanField(_('Is Accepted'),default=False)
    is_active         = models.BooleanField(_('Is Active'),default=True)

    class Meta      : 
        verbose_name = 'DriverRideRequest'
        verbose_name_plural = "DriverRideRequest"


    





class UserPermissions(Users):
    class Meta:
        proxy = True
        permissions = [('Can customer user permissions', 'access_customerpermissions')]


