from rest_framework import serializers
from ..models import PreEntrega, PreEntregaDet, DireccionEntrega



class DireccionEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionEntrega
        fields = '__all__'

class PreEntregaDetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreEntregaDet
        fields = '__all__'

class PreEntregaSerializer(serializers.ModelSerializer): 

    detalles = PreEntregaDetSerializer(many=True, read_only=True)
    direccion_entrega = DireccionEntregaSerializer(read_only=True)
    class Meta:
        model = PreEntrega
        fields = '__all__'