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
                 ,'version','kilos']
        
class EntregaDetSaldoSerializer(serializers.ModelSerializer):
    saldo = serializers.DecimalField(max_digits=10, decimal_places=2)
    cantidad_envio = serializers.DecimalField(max_digits=10, decimal_places=2)
    enviado = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model =EntregaDet
        fields= '__all__'
        read_only_fields = ['saldo','cantidad_envio','enviado']

class EntregaSerializer(serializers.ModelSerializer):
    detalles = EntregaDetSerializer(many = True)
    class Meta:
        model=  Entrega
        fields=  '__all__'

    
class EntregaSaldoSerializer(serializers.ModelSerializer):
    detalles = EntregaDetSaldoSerializer(many = True)
    class Meta:
        model = Entrega
        fields = '__all__'

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
    envio_id = serializers.IntegerField(required=False, allow_null=True)
    documento = serializers.IntegerField()
    tipo_documento = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    origen = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    fecha = serializers.DateTimeField()
    salida = serializers.DateTimeField(allow_null=True, required=False)
    arribo = serializers.DateTimeField(allow_null=True, required=False)
    recepcion = serializers.DateTimeField(allow_null=True, required=False)
    recibio = serializers.CharField()
    regreso = serializers.DateTimeField(allow_null=True, required=False)
    embarque = serializers.IntegerField()
    embarque_fecha = serializers.DateField()
    sucursal_embarque = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    operador = serializers.CharField()
    destinatario = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    direccion = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    detalles = EntregaDetsSeguimientoSerializer(many=True)

class ImgEntregaSerializer(serializers.ModelSerializer):
    entrega = EntregaSerializer()
    class Meta:
        model = ImgEntrega
        fields = '__all__'




