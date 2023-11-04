from rest_framework import serializers
from ..models import Operador, Sucursal


class OperadorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Operador
        fields = '__all__'


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model= Sucursal
        fields = ["id","clave","nombre"]