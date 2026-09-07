import uuid
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from ..models import Envio, EnvioDet, Entrega, EntregaDet, EnvioAnotaciones, InstruccionDeEnvio


def _generar_sx_unico(base=''):
    while True:
        suffix = uuid.uuid4().hex[:12]
        candidate = f"{base}-R-{suffix}" if base else f"R-{suffix}"
        candidate = candidate[:255]
        if not Envio.objects.filter(sx=candidate).exists() and not EnvioDet.objects.filter(sx=candidate).exists():
            return candidate


def _cantidad_asignada(detalle):
    return (
        EntregaDet.objects.filter(envio_det=detalle).aggregate(
            total=Coalesce(Sum('cantidad'), Decimal('0'))
        )['total']
        or Decimal('0')
    )


def partida_elegible_reasignacion(detalle):
    if not detalle.activo:
        return False, 'Partida ya reasignada'
    if detalle.clave == 'CORTE':
        return False, 'Partida de corte'
    if _cantidad_asignada(detalle) > 0:
        return False, 'Partida con asignación parcial'
    return True, None


def recalcular_totales_envio(envio):
    detalles = EnvioDet.objects.filter(envio=envio, activo=True).exclude(clave='CORTE')
    kilos = detalles.aggregate(total=Coalesce(Sum('me_kilos'), Decimal('0')))['total']
    valor = detalles.aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    envio.kilos = kilos
    envio.total_documento = valor
    envio.last_updated = timezone.now()
    envio.save(update_fields=['kilos', 'total_documento', 'last_updated'])


def _validar_envio_padre(envio):
    tipo_documento = (envio.tipo_documento or '').upper()
    if tipo_documento == 'COD':
        raise ValueError('No se puede reasignar un envío COD; solo CON o CRE')
    if tipo_documento not in ('CON', 'CRE'):
        raise ValueError('Solo se pueden reasignar envíos CON o CRE')
    if envio.envio_origen_id:
        raise ValueError('No se puede reasignar un envío derivado de reasignación')
    if envio.sucursal_entrega and envio.sucursal_entrega != envio.sucursal:
        raise ValueError('El envío ya está reasignado completamente')


def _copiar_instruccion(padre, hijo):
    instruccion = getattr(padre, 'instruccion', None)
    if not instruccion:
        return

    now = timezone.now()
    InstruccionDeEnvio.objects.create(
        envio=hijo,
        tipo=instruccion.tipo,
        contacto=instruccion.contacto,
        horario=instruccion.horario,
        telefono=instruccion.telefono,
        comentario=instruccion.comentario,
        direccion_calle=instruccion.direccion_calle,
        direccion_numero_exterior=instruccion.direccion_numero_exterior,
        direccion_numero_interior=instruccion.direccion_numero_interior,
        direccion_colonia=instruccion.direccion_colonia,
        direccion_codigo_postal=instruccion.direccion_codigo_postal,
        direccion_municipio=instruccion.direccion_municipio,
        direccion_estado=instruccion.direccion_estado,
        direccion_pais=instruccion.direccion_pais,
        direccion_latitud=instruccion.direccion_latitud,
        direccion_longitud=instruccion.direccion_longitud,
        fecha_de_entrega=instruccion.fecha_de_entrega,
        sx_transporte=instruccion.sx_transporte,
        sx=_generar_sx_unico(instruccion.sx or ''),
        distancia=instruccion.distancia,
        sector=instruccion.sector,
        date_created=now,
        last_updated=now,
        create_user=instruccion.create_user,
        update_user=instruccion.update_user,
        origen_sx=instruccion.origen_sx,
        version=instruccion.version,
        email_envio=instruccion.email_envio,
        tipo_envio=instruccion.tipo_envio,
        clasificcion_vale=instruccion.clasificcion_vale,
    )


def _crear_envio_hijo(padre, sucursal_entrega):
    now = timezone.now()
    hijo = Envio(
        sucursal=padre.sucursal,
        sucursal_entrega=sucursal_entrega,
        origen=padre.origen,
        entidad=padre.entidad,
        folio=padre.folio,
        fecha_documento=padre.fecha_documento,
        documento=padre.documento,
        tipo_documento=padre.tipo_documento,
        forma_pago=padre.forma_pago,
        pagado=padre.pagado,
        comentario=padre.comentario,
        callcenter=padre.callcenter,
        sx=_generar_sx_unico(padre.sx or ''),
        date_created=now,
        last_updated=now,
        create_user=padre.create_user,
        update_user=padre.update_user,
        version=padre.version,
        realizo=padre.realizo,
        destinatario=padre.destinatario,
        pasan=padre.pasan,
        usuario_pasan=padre.usuario_pasan,
        de_rfc_destinatario=padre.de_rfc_destinatario,
        de_destino=padre.de_destino,
        maniobra=padre.maniobra,
        email_envio=padre.email_envio,
        surtido=padre.surtido,
        uuid=padre.uuid,
        envio_origen=padre,
    )
    hijo.save()
    return hijo


def _clonar_detalle(detalle, hijo):
    now = timezone.now()
    return EnvioDet.objects.create(
        envio=hijo,
        origen_det_sx=detalle.origen_det_sx,
        producto_sx=detalle.producto_sx,
        clave=detalle.clave,
        me_descripcion=detalle.me_descripcion,
        me_kilos=detalle.me_kilos,
        valor=detalle.valor,
        moneda=detalle.moneda,
        me_cantidad=detalle.me_cantidad,
        instruccion_entrega=detalle.instruccion_entrega,
        sx=_generar_sx_unico(detalle.sx or ''),
        me_unidad=detalle.me_unidad,
        date_created=now,
        last_updated=now,
        create_user=detalle.create_user,
        update_user=detalle.update_user,
        version=detalle.version,
        cortes=detalle.cortes,
        kxmil=detalle.kxmil,
        me_bienes_transp=detalle.me_bienes_transp,
        me_clave_unidad=detalle.me_clave_unidad,
        me_material_peligroso=detalle.me_material_peligroso,
        surtido=detalle.surtido,
        surtidor=detalle.surtidor,
        activo=True,
    )


@transaction.atomic
def reasignar_partidas_envio(envio_id, sucursal_entrega, detalle_ids):
    if not sucursal_entrega:
        raise ValueError('Debe indicar la sucursal de entrega')

    padre = Envio.objects.select_related('instruccion').get(pk=envio_id)
    _validar_envio_padre(padre)

    if sucursal_entrega == padre.sucursal:
        raise ValueError('La sucursal de entrega debe ser distinta a la sucursal origen')

    if not detalle_ids:
        raise ValueError('Debe seleccionar al menos una partida')

    detalle_ids = list(dict.fromkeys(detalle_ids))
    detalles = list(
        EnvioDet.objects.filter(envio=padre, id__in=detalle_ids, activo=True).order_by('id')
    )

    if len(detalles) != len(detalle_ids):
        raise ValueError('Una o más partidas no pertenecen al envío o no están activas')

    for detalle in detalles:
        elegible, mensaje = partida_elegible_reasignacion(detalle)
        if not elegible:
            raise ValueError(f"Partida {detalle.clave}: {mensaje}")

    hijo = _crear_envio_hijo(padre, sucursal_entrega)
    _copiar_instruccion(padre, hijo)

    for detalle in detalles:
        _clonar_detalle(detalle, hijo)
        detalle.activo = False
        detalle.envio_hijo = hijo
        detalle.last_updated = timezone.now()
        detalle.save(update_fields=['activo', 'envio_hijo', 'last_updated'])

    recalcular_totales_envio(hijo)
    recalcular_totales_envio(padre)

    return hijo


def obtener_partidas_reasignacion(envio_id):
    envio = Envio.objects.get(pk=envio_id)
    _validar_envio_padre(envio)

    partidas = []
    for detalle in EnvioDet.objects.select_related('envio_hijo').filter(envio=envio).order_by('id'):
        elegible, motivo = partida_elegible_reasignacion(detalle)
        asignado = _cantidad_asignada(detalle)
        sucursal_reasignacion = None
        if not detalle.activo and detalle.envio_hijo_id and detalle.envio_hijo:
            sucursal_reasignacion = detalle.envio_hijo.sucursal_entrega
        partidas.append({
            'id': detalle.id,
            'clave': detalle.clave,
            'me_descripcion': detalle.me_descripcion,
            'me_cantidad': detalle.me_cantidad,
            'me_kilos': detalle.me_kilos,
            'activo': detalle.activo,
            'asignado': asignado,
            'elegible': elegible,
            'motivo_no_elegible': motivo,
            'reasignada': not detalle.activo and bool(detalle.envio_hijo_id),
            'sucursal_reasignacion': sucursal_reasignacion,
        })
    return partidas


def envio_hijo_tiene_asignaciones(hijo):
    if Entrega.objects.filter(envio=hijo).exists():
        return True
    hijo_det_ids = EnvioDet.objects.filter(envio=hijo).values_list('id', flat=True)
    if not hijo_det_ids:
        return False
    return EntregaDet.objects.filter(envio_det_id__in=hijo_det_ids).exists()


def _validar_gestion_envio_hijo(hijo_id):
    hijo = Envio.objects.select_related('envio_origen').get(pk=hijo_id)
    if not hijo.envio_origen_id:
        raise ValueError('No es un envío hijo de reasignación')
    if envio_hijo_tiene_asignaciones(hijo):
        raise ValueError('El envío hijo ya tiene asignaciones o está en un embarque')
    return hijo


@transaction.atomic
def cancelar_reasignacion_envio_hijo(envio_hijo_id):
    hijo = _validar_gestion_envio_hijo(envio_hijo_id)
    padre = hijo.envio_origen

    detalles_padre = list(
        EnvioDet.objects.filter(envio=padre, envio_hijo=hijo, activo=False)
    )
    if not detalles_padre:
        raise ValueError('No se encontraron partidas asociadas al envío hijo')

    now = timezone.now()
    for detalle in detalles_padre:
        detalle.activo = True
        detalle.envio_hijo = None
        detalle.last_updated = now
        detalle.save(update_fields=['activo', 'envio_hijo', 'last_updated'])

    InstruccionDeEnvio.objects.filter(envio=hijo).delete()
    EnvioAnotaciones.objects.filter(envio=hijo).delete()
    EnvioDet.objects.filter(envio=hijo).delete()
    hijo.delete()

    recalcular_totales_envio(padre)
    return padre


@transaction.atomic
def reasignar_destino_envio_hijo(envio_hijo_id, sucursal_entrega):
    hijo = _validar_gestion_envio_hijo(envio_hijo_id)
    if not sucursal_entrega:
        raise ValueError('Debe indicar la sucursal de entrega')
    if sucursal_entrega == hijo.sucursal:
        raise ValueError('La sucursal de entrega debe ser distinta a la sucursal origen')
    if sucursal_entrega == hijo.sucursal_entrega:
        raise ValueError('El envío ya está asignado a esa sucursal')

    hijo.sucursal_entrega = sucursal_entrega
    hijo.last_updated = timezone.now()
    hijo.save(update_fields=['sucursal_entrega', 'last_updated'])
    return hijo
