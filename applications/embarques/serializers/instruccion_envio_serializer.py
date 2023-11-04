from rest_framework import serializers
from ..models import InstruccionDeEnvio


class InstruccionEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model= InstruccionDeEnvio
        fields= ['id','direccion_latitud','direccion_longitud','direccion_calle','direccion_numero_interior','direccion_numero_exterior','direccion_colonia','direccion_codigo_postal',
                 'direccion_municipio', 'direccion_estado','direccion_pais' ]
