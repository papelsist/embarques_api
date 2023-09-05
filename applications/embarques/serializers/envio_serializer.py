from rest_framework import serializers
from datetime import datetime
from ..models import Envio
from .envio_det_serializer import EnvioDetSerializer
from applications.shared.utils.date_utils import  DateUtils


class EnvioSerializerEm(serializers.ModelSerializer):
    detalles = EnvioDetSerializer(many= True)
    class Meta:
        model= Envio
        fields= ['id','documento','fecha_documento','sucursal','tipo_documento','destinatario','detalles' ]
        #tefields = '__all__'

class EnvioSerializer(serializers.ModelSerializer):
    partidas  = serializers.IntegerField()
    retraso = serializers.SerializerMethodField()
    class Meta:
        model= Envio
        fields = ['id','documento', 'fecha_documento','sucursal','tipo_documento','forma_pago','de_destinatario','date_created','de_destinatario','partidas','retraso']
   
    def get_retraso(self,obj):
        time_lapse = DateUtils.get_time_lapse_now(obj.date_created)
        return time_lapse
    
