from rest_framework import serializers
from ..models import Embarque
from .operador_serializer import OperadorSerializer
from .entrega_serializer import EntregaSerializer


class EmbarqueSerializer(serializers.ModelSerializer):
    operador = OperadorSerializer()
    partidas = EntregaSerializer(many = True)
    class Meta:
        model= Embarque
        fields = '__all__'