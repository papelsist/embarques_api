from rest_framework import serializers
from ..models import EnvioDet


class EnvioDetSerializer(serializers.ModelSerializer):
    class Meta:
        model =  EnvioDet
        fields = ['id','clave','me_descripcion','me_cantidad','valor','me_kilos','saldo','cortes']

