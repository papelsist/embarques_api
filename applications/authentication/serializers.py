from rest_framework import serializers
from .models import User 
from applications.embarques.serializers.catalogos_serializer import SucursalSerializer
from django.contrib.auth.models import Permission, Group





class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Permission
        fields = ["id","codename"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model= Group
        fields = ["id","name"]


class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many= True)
    groups = GroupSerializer(many= True)
    sucursal = SucursalSerializer()
    class Meta:
        model= User
        fields = ["id","nombre","nombres","username","sucursal","user_permissions","groups"]
       
