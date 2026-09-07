from rest_framework import serializers
from ..models import EnvioDet


class EnvioDetReasignacionMixin(serializers.Serializer):
    sucursal_reasignacion = serializers.SerializerMethodField()
    reasignada = serializers.SerializerMethodField()

    def get_sucursal_reasignacion(self, obj):
        if obj.activo:
            return None
        if obj.envio_hijo_id and obj.envio_hijo:
            return obj.envio_hijo.sucursal_entrega
        return None

    def get_reasignada(self, obj):
        return not obj.activo and bool(obj.envio_hijo_id)


class EnvioDetSerializer(EnvioDetReasignacionMixin, serializers.ModelSerializer):
    class Meta:
        model = EnvioDet
        fields = [
            'id', 'clave', 'me_descripcion', 'me_cantidad', 'valor', 'me_kilos',
            'cortes', 'surtido', 'activo', 'sucursal_reasignacion', 'reasignada',
        ]


class EnvioDetSaldoSerializer(EnvioDetReasignacionMixin, serializers.ModelSerializer):
    saldo = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    asignado = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = EnvioDet
        fields = '__all__'
        read_only_fields = ['saldo', 'asignado']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sucursal_reasignacion'] = self.get_sucursal_reasignacion(instance)
        data['reasignada'] = self.get_reasignada(instance)
        return data
