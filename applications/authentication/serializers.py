from rest_framework import serializers
from .models import User 
from applications.embarques.serializers.catalogos_serializer import SucursalSerializer
from django.contrib.auth.models import Permission





class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Permission
        fields = ["id","codename"]


class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many= True)
    sucursal = SucursalSerializer()
    class Meta:
        model= User
        fields = ["id","nombre","nombres","username","sucursal","user_permissions"]
       
