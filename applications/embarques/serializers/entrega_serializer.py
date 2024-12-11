from rest_framework import serializers
from ..models import Entrega, EntregaDet, EntregaIncidencia, EntregaIncidenciaSeguimiento, ImgEntrega
from .envio_serializer import EnvioRutaSerializer



class IncidenciaSeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaIncidenciaSeguimiento
        fields = '__all__'

class IncidenciaSerializer(serializers.ModelSerializer):
    seguimientos = IncidenciaSeguimientoSerializer(many = True)
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


class EntregaDetsSeguimientoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    clave = serializers.CharField()
    descripcion = serializers.CharField()
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=2)

class EntregaSeguimientoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    documento = serializers.IntegerField()
    fecha = serializers.DateTimeField()
    salida = serializers.DateTimeField()
    arribo = serializers.DateTimeField()
    recepcion = serializers.DateTimeField()
    recibio = serializers.CharField()
    regreso = serializers.DateTimeField()
    embarque = serializers.IntegerField()
    embarque_fecha = serializers.DateField()
    operador = serializers.CharField()
    detalles = EntregaDetsSeguimientoSerializer(many = True)

class ImgEntregaSerializer(serializers.ModelSerializer):
    entrega = EntregaSerializer()
    class Meta:
        model = ImgEntrega
        fields = '__all__'




