from rest_framework import serializers
from ..models import Entrega, EntregaDet




class EntregaDetSerializer(serializers.ModelSerializer):
    class Meta:
        model =EntregaDet
        fields= ['id','entrega','envio_det','sx_instruccion_de_envio','almacen','instruccion_de_entrega_parcial','clave'
                 ,'descripcion','cantidad','valor', 'comentario','date_created','last_updated'
                 ,'version','saldo','cantidad_envio','enviado']

class EntregaSerializer(serializers.ModelSerializer):
    detalles = EntregaDetSerializer(many = True)
    class Meta:
        model=  Entrega
        fields=  '__all__'



