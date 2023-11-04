from rest_framework import serializers
from applications.embarques.serializers import EmbarqueSerializer, EnvioSerializerEm


class RutaSerializer(serializers.Serializer):
    embarque = EmbarqueSerializer()
    destinos = EnvioSerializerEm(many = True)
    ocupado = serializers.FloatField()

class RutasSerializer(serializers.Serializer):
   
   no_asignados = EnvioSerializerEm(many=True)
   outliers = EnvioSerializerEm(many = True)
   rutas = RutaSerializer(many= True)


   



