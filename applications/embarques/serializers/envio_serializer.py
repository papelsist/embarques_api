from rest_framework import serializers
from datetime import datetime
from ..models import Envio, EnvioAnotaciones
from .envio_det_serializer import EnvioDetSerializer
from .instruccion_envio_serializer import InstruccionEnvioSerializer
from applications.shared.utils.date_utils import  DateUtils


class AnotacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model= EnvioAnotaciones
        fields = '__all__'

class EnvioSerializerEm(serializers.ModelSerializer):
    detalles = EnvioDetSerializer(many= True)
    instruccion = InstruccionEnvioSerializer()
    anotaciones = AnotacionesSerializer(many=True)
    class Meta:
        model= Envio
        fields= ['id','documento','fecha_documento','sucursal','tipo_documento','destinatario','detalles','saldo', 'kilos','instruccion','pasan','usuario_pasan','date_created','anotaciones','surtido','pagado' ]
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

class EnvioSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model= Envio
        fields = '__all__'
    



class EnvioAnotacionesSerializer(serializers.ModelSerializer):
    anotaciones = AnotacionesSerializer(many=True)
    instruccion = InstruccionEnvioSerializer()
    class Meta:
        model= Envio
        fields= ['id','documento','fecha_documento','sucursal','tipo_documento','destinatario','detalles','saldo', 'kilos','instruccion','anotaciones','pasan','usuario_pasan','date_created' ]

    
