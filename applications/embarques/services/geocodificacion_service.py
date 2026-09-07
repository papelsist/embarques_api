import logging
import os
import re
import unicodedata

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

logger = logging.getLogger(__name__)


def _normalizar_texto(valor):
    if valor is None:
        return ''
    texto = str(valor).strip().casefold()
    texto = ''.join(
        caracter
        for caracter in unicodedata.normalize('NFD', texto)
        if unicodedata.category(caracter) != 'Mn'
    )
    texto = re.sub(r'[^a-z0-9]+', ' ', texto)
    return ' '.join(texto.split())


def _normalizar_codigo_postal(valor):
    if valor is None:
        return ''
    return re.sub(r'\D', '', str(valor).strip())


def direccion_coincide_con_cliente(instruccion, cliente):
    calle_instruccion = _normalizar_texto(instruccion.direccion_calle)
    calle_cliente = _normalizar_texto(cliente.direccion_calle)
    cp_instruccion = _normalizar_codigo_postal(instruccion.direccion_codigo_postal)
    cp_cliente = _normalizar_codigo_postal(cliente.direccion_codigo_postal)
    if not calle_instruccion or not calle_cliente or not cp_instruccion or not cp_cliente:
        return False
    return calle_instruccion == calle_cliente and cp_instruccion == cp_cliente


def construir_query_direccion(
    calle=None,
    numero_exterior=None,
    colonia=None,
    municipio=None,
    estado=None,
    codigo_postal=None,
    pais='México',
):
    calle_numero = ' '.join(str(parte).strip() for parte in [calle, numero_exterior] if parte)
    partes = [
        calle_numero,
        colonia,
        municipio,
        estado,
        codigo_postal,
        pais or 'México',
    ]
    return ', '.join(str(parte).strip() for parte in partes if parte and str(parte).strip())


def get_coordenadas_de_campos(data, prefijo=''):
    query = construir_query_direccion(
        calle=data.get(f'{prefijo}calle'),
        numero_exterior=data.get(f'{prefijo}numero_exterior'),
        colonia=data.get(f'{prefijo}colonia'),
        municipio=data.get(f'{prefijo}municipio'),
        estado=data.get(f'{prefijo}estado'),
        codigo_postal=data.get(f'{prefijo}codigo_postal'),
        pais=data.get(f'{prefijo}pais') or 'México',
    )
    return get_coordenadas(query)


def get_coordenadas(direccion):
    try:
        if not direccion or not str(direccion).strip():
            return None, None

        token = (os.getenv('MAPBOX_TOKEN') or '').strip()
        if not token:
            logger.warning('MAPBOX_TOKEN no configurado; no se geocodificó la dirección')
            return None, None

        response = requests.get(
            'https://api.mapbox.com/search/geocode/v6/forward',
            params={
                'q': direccion,
                'access_token': token,
                'country': 'mx',
                'limit': 1,
                'language': 'es',
            },
            timeout=8,
        )
        response.raise_for_status()
        features = (response.json() or {}).get('features') or []
        if not features:
            logger.warning('Mapbox no devolvió coordenadas para: %s', direccion)
            return None, None

        coordinates = features[0].get('geometry', {}).get('coordinates') or []
        if len(coordinates) < 2:
            return None, None

        longitud, latitud = coordinates[0], coordinates[1]
        return latitud, longitud
    except Exception:
        logger.exception('Error al geocodificar la dirección: %s', direccion)
        return None, None


def geocodificar_instruccion_y_cliente(envio_id):
    from applications.core.models import Cliente
    from applications.embarques.models import Envio

    envio = Envio.objects.select_related('instruccion').get(pk=envio_id)
    try:
        instruccion = envio.instruccion
    except ObjectDoesNotExist:
        raise ValueError('El envío no tiene instrucción de envío')

    latitud, longitud = get_coordenadas_de_campos({
        'calle': instruccion.direccion_calle,
        'numero_exterior': instruccion.direccion_numero_exterior,
        'colonia': instruccion.direccion_colonia,
        'municipio': instruccion.direccion_municipio,
        'estado': instruccion.direccion_estado,
        'codigo_postal': instruccion.direccion_codigo_postal,
        'pais': instruccion.direccion_pais or 'México',
    })
    if latitud is None or longitud is None:
        raise ValueError('No se encontraron coordenadas para la dirección de la instrucción')

    instruccion.direccion_latitud = latitud
    instruccion.direccion_longitud = longitud
    instruccion.last_updated = timezone.now()
    instruccion.save(update_fields=['direccion_latitud', 'direccion_longitud', 'last_updated'])

    rfc = (envio.de_rfc_destinatario or '').strip()
    clientes_actualizados = 0
    clientes_omitidos = 0
    if rfc:
        clientes = Cliente.objects.filter(rfc__iexact=rfc)
        for cliente in clientes:
            if not direccion_coincide_con_cliente(instruccion, cliente):
                clientes_omitidos += 1
                logger.info(
                    'No se actualizó cliente %s: calle/CP distintos a la instrucción del envío %s',
                    cliente.id,
                    envio.id,
                )
                continue
            cliente.direccion_latitud = latitud
            cliente.direccion_longitud = longitud
            cliente.save(update_fields=['direccion_latitud', 'direccion_longitud', 'last_updated'])
            clientes_actualizados += 1

    return {
        'envio_id': envio.id,
        'latitud': latitud,
        'longitud': longitud,
        'rfc': rfc or None,
        'cliente_actualizado': clientes_actualizados > 0,
        'clientes_actualizados': clientes_actualizados,
        'clientes_omitidos': clientes_omitidos,
    }
