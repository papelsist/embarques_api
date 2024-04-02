from rest_framework import serializers
from ..models import Entrega, EntregaDet, EntregaIncidencia
from .envio_serializer import EnvioRutaSerializer



class IncidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaIncidencia
        fields = '__all__'

class EntregaDetSerializer(serializers.ModelSerializer):
    class Meta:
        model =EntregaDet
        fields= ['id','entrega','envio_det','sx_instruccion_de_envio','almacen','instruccion_de_entrega_parcial','clave'
                 ,'descripcion','cantidad','valor', 'comentario','date_created','last_updated'
                 ,'version','saldo','cantidad_envio','enviado','kilos']

class EntregaSerializer(serializers.ModelSerializer):
    detalles = EntregaDetSerializer(many = True)
    class Meta:
        model=  Entrega
        fields=  '__all__'

class EntregaRutaSerializer(serializers.ModelSerializer):
    envio = EnvioRutaSerializer()
    detalles = EntregaDetSerializer(many = True)
    class Meta:
        model=  Entrega
        fields=  '__all__'




