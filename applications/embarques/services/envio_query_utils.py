from django.db.models import Q, F

from ..models import EnvioDet


def filtro_envio_tablero_origen():
    """Excluye envíos reasignados a otra sucursal (incluye envíos hijo)."""
    return (
        Q(envio__sucursal_entrega__isnull=True)
        | Q(envio__sucursal_entrega='')
        | Q(envio__sucursal_entrega=F('envio__sucursal'))
    )


def queryset_detalles_activos():
    return EnvioDet.objects.filter(activo=True)


def queryset_detalles_con_reasignacion():
    return EnvioDet.objects.select_related('envio_hijo').all()
