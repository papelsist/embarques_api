from rest_framework import serializers
from ..models import Envio

class EnvioSerializer(serializers.Serializer):
    documento = serializers.CharField()
    fecha_documento = serializers.DateTimeField()
    sucursal = serializers.CharField()
    tipo_documento = serializers.CharField()
    forma_pago = serializers.CharField()
   