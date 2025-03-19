from ..models import Embarque, Envio,EnvioDet, Entrega, EntregaDet
from decimal import Decimal
import requests

def crear_entrega_traslado_envio(embarque_id, envio, data,traslado):

    embarque = Embarque.objects.get(id=embarque_id)
    entrega = Entrega(
                    envio=envio,
                    embarque=embarque,
                    sucursal = envio.sucursal,
                    destinatario = envio.destinatario,
                    operador = embarque.operador.nombre,
                    entidad = envio.entidad,
                    fecha_documento = envio.fecha_documento,
                    documento = envio.documento,
                    tipo_documento = envio.tipo_documento,
                    origen = envio.origen
                    )

    entrega.save()

    kilos_embarque = embarque.kilos
    kilos_entrega = 0
    valor_entrega = 0
    for det in data:
        envio_det = EnvioDet.objects.get(id = det['envio_det_id'])
        enviar = det['enviar']
        
        kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
        valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))

        
        entrega_det = EntregaDet(
                    entrega= entrega,
                    envio_det = envio_det,
                    clave = envio_det.clave,
                    descripcion = envio_det.me_descripcion,
                    cantidad = enviar,
                    valor = valor_envio,
                    kilos = kilos_envio
        ) 

        entrega_det.save()

        kilos_entrega += kilos_envio
        valor_entrega += valor_envio
        kilos_embarque += kilos_entrega

    entrega.kilos = kilos_entrega
    entrega.valor = valor_entrega
    entrega.save()

    embarque.kilos = kilos_embarque
    embarque.save()


        

    
