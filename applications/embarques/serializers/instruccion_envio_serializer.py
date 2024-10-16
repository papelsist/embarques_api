from rest_framework import serializers
from ..models import InstruccionDeEnvio, TransporteForaneo, GeolocalizacionTransportes  


class GeolocalizacionTransportesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeolocalizacionTransportes
        fields = '__all__'


class TransporteForaneoSerializer(serializers.ModelSerializer):
    ubicaciones = GeolocalizacionTransportesSerializer(many=True)
    class Meta:
        model= TransporteForaneo
        fields = ['id','direccion_latitud','direccion_longitud','direccion_calle','direccion_numero_interior','direccion_numero_exterior','direccion_colonia','direccion_codigo_postal',
                 'direccion_municipio', 'direccion_estado','direccion_pais','ubicaciones' ]

class InstruccionEnvioSerializer(serializers.ModelSerializer):
    sx_transporte = TransporteForaneoSerializer()
    class Meta:
        model= InstruccionDeEnvio
        fields= ['id','direccion_latitud','direccion_longitud','direccion_calle','direccion_numero_interior','direccion_numero_exterior','direccion_colonia','direccion_codigo_postal',
                 'direccion_municipio', 'direccion_estado','direccion_pais','fecha_de_entrega','sector','distancia','sx_transporte' ]
