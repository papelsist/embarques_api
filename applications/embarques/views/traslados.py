from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Envio
from applications.commons.sql_dao import fix_id_to_sql
from decimal import Decimal
from ..services import crear_entrega_traslado_envio


@api_view(['POST'])
def crear_entrega_traslado(request):
    traslado_dict = request.data
    traslado = request.data["traslado"]
    print(traslado)
    venta = request.data["venta"]
    embarque_id = request.data["embarque_id"]
    print(venta)
    envio = Envio.objects.get(sx=venta)
    detalles = envio.detalles.all()
    detalles_dict = request.data['detalles']
    partidas_envio_dict = []
    for detalle in detalles:
        for detalle_dict in detalles_dict:
            if detalle.producto_sx == fix_id_to_sql(detalle_dict['producto_id']):
                det = {
                    "envio_det_id": detalle.id,
                    "enviar": -Decimal(detalle_dict['enviar']) 
                }
                partidas_envio_dict.append(det)
    print(embarque_id)
    crear_entrega_traslado_envio(embarque_id,envio,partidas_envio_dict,traslado)



    return Response(traslado_dict)