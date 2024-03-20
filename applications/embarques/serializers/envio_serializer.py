from rest_framework import serializers
from datetime import datetime
from ..models import Envio
from .envio_det_serializer import EnvioDetSerializer
from .instruccion_envio_serializer import InstruccionEnvioSerializer
from applications.shared.utils.date_utils import  DateUtils


class EnvioSerializerEm(serializers.ModelSerializer):
    detalles = EnvioDetSerializer(many= True)
    instruccion = InstruccionEnvioSerializer()
    class Meta:
        model= Envio
        fields= ['id','documento','fecha_documento','sucursal','tipo_documento','destinatario','detalles','saldo', 'kilos','instruccion' ]
        #tefields = '__all__'

class EnvioSerializer(serializers.ModelSerializer):
    partidas  = serializers.IntegerField()
    retraso = serializers.SerializerMethodField()
    class Meta:
        model= Envio
        fields = ['id','documento', 'fecha_documento','sucursal','tipo_documento','forma_pago','destinatario','date_created','de_destinatario','partidas','retraso']
   
    def get_retraso(self,obj):
        time_lapse = DateUtils.get_time_lapse_now(obj.date_created)
        return time_lapse
    
class EnvioRutaSerializer(serializers.ModelSerializer):
    instruccion = InstruccionEnvioSerializer()
    class Meta:
        model= Envio
        fields = ['id','destinatario','detalles','documento','fecha_documento','tipo_documento','sucursal','instruccion']
    

    
