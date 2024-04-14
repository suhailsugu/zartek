
from rest_framework import serializers
from apps.users.models import Users







class LoginPostSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email','password']

class LoginSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email','username','is_admin', 'is_active', 'is_verified', 'is_superuser']

