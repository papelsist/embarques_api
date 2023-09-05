from rest_framework import serializers
from ..models import Entrega, EntregaDet




class EntregaDetSerializer(serializers.ModelSerializer):
    class Meta:
        model =EntregaDet
        fields= '__all__'

class EntregaSerializer(serializers.ModelSerializer):
    detalles = EntregaDetSerializer(many = True)
    class Meta:
        model=  Entrega
        fields=  '__all__'



