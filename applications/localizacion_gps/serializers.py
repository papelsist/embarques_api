from rest_framework import serializers
from applications.embarques.serializers import EmbarqueSerializer, TransporteSerializer, EmbarqueRutaSerializer


class UbicacionGPSSerializer(serializers.Serializer):

    imei = serializers.CharField(max_length=50)
    operador = serializers.CharField(max_length=150)
    transporte = TransporteSerializer() 
    embarque = EmbarqueRutaSerializer()
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    speed = serializers.FloatField()
    course = serializers.IntegerField()