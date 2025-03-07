from rest_framework import serializers
from ..models import Operador, Sucursal, DireccionEntrega,TransporteEmbarques


class OperadorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Operador
        fields = '__all__'


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model= Sucursal
        fields = ["id","clave","nombre","direccion_latitud","direccion_longitud"]

class DireccionEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model= DireccionEntrega
        fields = '__all__'

class TransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model= TransporteEmbarques
        fields = '__all__'