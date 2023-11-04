from ..models import Embarque,Entrega,EntregaDet,Envio,EnvioDet
from datetime import datetime



def salvar_embarque(embarque_dict):
    """ Funcion para actualizar un embarque despues de haberlo creado 

    Args:
        embarque_dict (_type_): _description_
    """
 
    embarque = Embarque.objects.get(id = embarque_dict['embarqueId'])
    embarque.cp = embarque_dict['cp']
    embarque.save()
    for ent in embarque_dict['partidas']:
        envio = Envio.objects.get(id = ent['envioId'])

        try:
            entrega  = Entrega.objects.get(id = ent['entregaId'])
        except Entrega.DoesNotExist as e:
            entrega = Entrega(
                        envio=envio,
                        embarque=embarque,
                        sucursal = embarque.sucursal.nombre,
                        destinatario = ent['destinatario'],
                        operador = embarque.operador.nombre,
                        entidad = ent['entidad'],
                        fecha_documento = ent['fechaDocumento'],
                        documento = ent['documento'],
                        tipo_documento = ent['tipoDocumento'],
                        origen = ent['tipoDocumento']
                        )
        finally:
            entrega.save()

        for det in ent['detalles']:
            envio_det = EnvioDet.objects.get(id = det['id'])
            try:
                entrega_det = EntregaDet.objects.get(id = det['entregaDetId'])
                entrega_det.cantidad = det['enviar']
            except EntregaDet.DoesNotExist as e:
                print(e)
                entrega_det = EntregaDet(
                    entrega= entrega,
                    envio_det = envio_det,
                    clave = det['clave'],
                    descripcion = det['me_descripcion'],
                    cantidad = det['enviar'],
                    valor = det['valor']
                )
            finally:
                entrega_det.save()

def borrar_entrega_det(entrega_det_dict):
    if entrega_det_dict['entregaDetId'] :
        entrega_det = EntregaDet.objects.get(id = entrega_det_dict['entregaDetId'] )     
        entrega_det_deleted = entrega_det.delete() 
        if entrega_det_deleted[0] >=1:
            entrega = Entrega.objects.get(id =entrega_det_dict['entregaId']  )
            detalles = entrega.detalles.all()
            if len(detalles) <= 0:
                entrega.delete() 
        return entrega_det_deleted[0] 
    else: 
        return 0
    

def registrar_salida_embarque(embarque_dict):
    embarque = Embarque.objects.get(id = embarque_dict['id'])
    embarque.or_fecha_hora_salida = datetime.now()
    embarque.save()
    return embarque

def borrar_embarque(embarque_dict):
    embarque = Embarque.objects.get(id = embarque_dict['id'])
    if len(embarque.partidas.all())==0:
        print('Borrar Embarque !!!')
        embarque_deleted = embarque.delete()
        return embarque_deleted[0] 
    else: 
        return 0
    
def actualizar_bitacora_embarque(embarque_dict):
    embarque = Embarque.objects.get(id = embarque_dict['id'])
    partidas_dict = embarque_dict['partidas']

    for partida in partidas_dict:
        entrega = Entrega.objects.get(id = partida['entregaId'])
        entrega.arribo = partida['arribo']
        entrega.arribo_latitud = partida['arribo_latitud']
        entrega.arribo_longitud = partida['arribo_longitud']
        entrega.recepcion = partida['recepcion']
        entrega.recepcion_latitud = partida['recepcion_latitud']
        entrega.recepcion_longitud = partida['recepcion_longitud']
        entrega.recibio = partida['recibio']
        entrega.save()

    return embarque

def eliminar_entrega_embarque(entrega_dict):
    entrega = Entrega.objects.get(id = entrega_dict['entregaId'])
    entrega_deleted = entrega.delete()
    if entrega_deleted[0] >=1:
        return entrega_deleted[0] 
    else: 
        return 0
    

def registrar_regreso_embarque(embarque_dict):
    embarque = Embarque.objects.get(id=embarque_dict['id'])

    partidas = embarque.partidas.all().filter(recepcion = None )
    print(len(partidas))
    if len(partidas) == 0:
        print("Registrando el regreso")
        embarque.regreso=  datetime.now()
        embarque.save()
        actualizado = 1
    else:
        actualizado = 0
    return embarque, actualizado


def crear_embarque_por_ruteo(ruta):
    #print(ruta)
    embarque_id = ruta['embarque']['id']
    print(embarque_id)
    destinos = ruta['destinos']
    embarque = Embarque.objects.get(pk=embarque_id)
    print(embarque)
    for destino in destinos:
        print("*"*50)
        print(destino['id'])
        envio = Envio.objects.get(pk=destino['id'])
        print(envio)
        entrega = Entrega(
                        envio=envio,
                        embarque=embarque,
                        sucursal = embarque.sucursal.nombre,
                        destinatario = envio.destinatario,
                        operador = embarque.operador.nombre,
                        entidad = envio.entidad,
                        fecha_documento = envio.fecha_documento,
                        documento = envio.documento,
                        tipo_documento = envio.tipo_documento,
                        origen = envio.tipo_documento
                        )
        entrega.save()
        for det in envio.detalles.all():
            if det.clave != 'CORTE':
                print(det)
                entrega_det = EntregaDet(
                        entrega= entrega,
                        envio_det = det,
                        clave = det.clave,
                        descripcion = det.me_descripcion,
                        cantidad = det.me_cantidad,
                        valor = det.valor
                    )
                entrega_det.save()
    embarque.save()

    
    