from rest_framework.serializers import ModelSerializer
from .models import CodigosPostalesMX, Cliente


class CodigosPostalesSerializer(ModelSerializer):
    class Meta:
        model = CodigosPostalesMX
        fields = '__all__'


class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'clave', 'nombre', 'rfc', 'razon_social']