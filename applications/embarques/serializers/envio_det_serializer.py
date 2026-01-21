from rest_framework import serializers
from ..models import EnvioDet


class EnvioDetSerializer(serializers.ModelSerializer):
    class Meta:
        model =  EnvioDet
        fields = ['id','clave','me_descripcion','me_cantidad','valor','me_kilos','cortes','surtido']

class EnvioDetSaldoSerializer(serializers.ModelSerializer):
    saldo = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    asignado = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model =  EnvioDet
        fields = '__all__'
        read_only_fields = ['saldo', 'asignado']

