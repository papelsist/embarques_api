from rest_framework import serializers
from ..models import Embarque
from .operador_serializer import OperadorSerializer
from .entrega_serializer import EntregaSerializer,EntregaRutaSerializer, EntregaSaldoSerializer


class EmbarqueSerializer(serializers.ModelSerializer):
    operador = OperadorSerializer()
    partidas = EntregaSerializer(many = True)
    class Meta:
        model= Embarque
        fields = '__all__'

class EmbarqueSaldoSerializer(serializers.ModelSerializer):
    operador = OperadorSerializer()
    partidas = EntregaSaldoSerializer(many = True)
    class Meta:
        model = Embarque
        fields = '__all__'


class EmbarqueBasicSerializer(serializers.ModelSerializer):
    operador = OperadorSerializer()
    
    class Meta:
        model= Embarque
        fields = ['id', 'documento', 'fecha', 'operador', 'sucursal', 'facturista', 'comentario', 'or_fecha_hora_salida', 'regreso','partidas']
        fields


class EmbarqueRutaSerializer(serializers.ModelSerializer):
    operador = OperadorSerializer()
    partidas = EntregaRutaSerializer(many = True)
    class Meta:
        model= Embarque
        fields = '__all__'


class EmbarqueOperadorSerializer(serializers.Serializer):
    operador__id = serializers.IntegerField()
    operador__nombre = serializers.CharField()
    fecha_inicial = serializers.DateField()
    fecha_final = serializers.DateField()
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)

class EmbarqueSingleSerializer(serializers.ModelSerializer):
    operador = OperadorSerializer()
    class Meta:
        model= Embarque
        fields = '__all__'
  
   
