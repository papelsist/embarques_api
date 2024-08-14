from ..models import Embarque,Entrega,EntregaDet,Envio,EnvioDet, EntregaIncidencia, ImgEntrega, Folio
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from decimal import Decimal



def salvar_embarque(embarque_dict):
    """ Funcion para actualizar un embarque despues de haberlo creado 

    Args:
        embarque_dict (_type_): _description_
    """
 
    embarque = Embarque.objects.get(id = embarque_dict['embarqueId'])
    embarque.cp = embarque_dict['cp']
    
    embarque.save()
    kilos_embarque = 0
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

        kilos_entrega = 0
        valor_entrega = 0
        print("Kilos entrega: ", kilos_entrega)
        for det in ent['detalles']:
            envio_det = EnvioDet.objects.get(id = det['id'])
            enviar = Decimal(det['enviar'])
            
            kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
            valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))
            print("Enviar: ", enviar)
            print("Valor envio: ", valor_envio)
            print(type(valor_envio))
            try:
                entrega_det = EntregaDet.objects.get(id = det['entregaDetId'])
                entrega_det.cantidad = det['enviar']
                entrega_det.kilos = kilos_envio
                entrega_det.valor = valor_envio
            except EntregaDet.DoesNotExist as e:
                print("Tratando de crear un detalle no existente")
                entrega_det = EntregaDet(
                    entrega= entrega,
                    envio_det = envio_det,
                    clave = det['clave'],
                    descripcion = det['me_descripcion'],
                    cantidad = det['enviar'],
                    valor = valor_envio,
                    kilos = kilos_envio
                )
            finally:
                entrega_det.save()
            kilos_entrega += kilos_envio
            valor_entrega += valor_envio
            print("Kilos entrega__: ", kilos_entrega)
        entrega.kilos = kilos_entrega
        entrega.valor = valor_entrega
        print("Entrega kilos: ", entrega.kilos)
        print("Entrega valor: ", entrega.valor)
        entrega.save()
        kilos_embarque += kilos_entrega
    embarque.kilos = kilos_embarque
    embarque.save()

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
        embarque_deleted = embarque.delete()
        return embarque_deleted[0] 
    else: 
        return 0
    
def actualizar_bitacora_embarque(embarque_dict):
    embarque = Embarque.objects.get(id = embarque_dict['id'])
    partidas_dict = embarque_dict['partidas']
    for partida in partidas_dict:
        entrega = Entrega.objects.get(id = partida['entregaId'])
        entrega.arribo = partida["arribo"] if "arribo" in partida else None
        entrega.arribo_latitud = partida["arribo_latitud"] if "arribo_latitud" in partida else None
        entrega.arribo_longitud = partida["arribo_longitud"] if "arribo_longitud" in partida else None
        entrega.recepcion = partida["recepcion"] if "recepcion" in partida else None
        entrega.recepcion_latitud = partida["recepcion_latitud"] if "recepcion_latitud" in partida else None
        entrega.recepcion_longitud = partida["recepcion_longitud"] if  "recepcion_longitud" in partida else None
        entrega.recibio = partida["recibio"] if "recibio" in partida else None

        if 'imagenes' in partida:
            imagenes = partida['imagenes']
            for imagen in imagenes:
                img = ImgEntrega()
                img.url_image = imagen
                img.entrega = entrega
                img.save()
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
        embarque.regreso=  datetime.now()
        embarque.save()
        actualizado = 1
    else:
        actualizado = 0
    return embarque, actualizado


def crear_embarque_por_ruteo(ruta):
    embarque_id = ruta['embarque']['id']
    destinos = ruta['destinos']
    embarque = Embarque.objects.get(pk=embarque_id)
    kilos_embarque = 0
    for destino in destinos:
        envio = Envio.objects.get(pk=destino['id'])
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
        kilos_entrega = 0
        valor_entrega = 0
        print("Kilos entrega: ", kilos_entrega)

        for det in envio.detalles.all():
            if det.clave != 'CORTE':
                envio_det = EnvioDet.objects.get(pk = det.id)
                enviar = Decimal(det.me_cantidad)
                kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
                valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))
                entrega_det = EntregaDet(
                        entrega= entrega,
                        envio_det = det,
                        clave = det.clave,
                        descripcion = det.me_descripcion,
                        cantidad = det.me_cantidad,
                        valor = valor_envio,
                    )
                entrega_det.save()
                kilos_entrega += kilos_envio
                valor_entrega += valor_envio
                print("Kilos entrega__: ", kilos_entrega)
        entrega.kilos = kilos_entrega
        entrega.valor = valor_entrega
        print("Entrega kilos: ", entrega.kilos)
        entrega.save()
        kilos_embarque += kilos_entrega
    embarque.kilos = kilos_embarque
    embarque.save()


def asignar_envios_pendientes(data):
    print(data)
    embarque = Embarque.objects.get(pk=data['embarque_id'])
    print(embarque)
    kilos_embarque = 0
    for env in data['envios']:
        print(env)
        envio = Envio.objects.get(pk=env)
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
        kilos_entrega = 0
        valor_entrega = 0
        print("Kilos entrega: ", kilos_entrega)
        
        for det in envio.detalles.all():
            if det.clave != 'CORTE':
                print(det)
                envio_det = EnvioDet.objects.get(pk = det.id)
                enviar = Decimal(det.me_cantidad)
                kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
                valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))
                entrega_det = EntregaDet(
                        entrega= entrega,
                        envio_det = det,
                        clave = det.clave,
                        descripcion = det.me_descripcion,
                        cantidad = det.saldo,
                        valor = valor_envio,
                        kilos = kilos_envio
                    )
                entrega_det.save()
                kilos_entrega += kilos_envio
                valor_entrega += valor_envio

                print("Kilos entrega__: ", kilos_entrega)
        entrega.kilos = kilos_entrega
        entrega.valor = valor_entrega
        print("Entrega kilos: ", entrega.kilos)
        entrega.save()
        kilos_embarque += kilos_entrega
    embarque.kilos = kilos_embarque
    embarque.save()


def crear_incidencia_entrega_det( entrega_det_id, incidencia_dict, request):

    user = get_user_logged(request)
    
    entrega_det = EntregaDet.objects.get(pk=entrega_det_id)
    envio = entrega_det.entrega.envio
    entrega = entrega_det.entrega
    incidencia = EntregaIncidencia()
    incidencia.envio = envio
    folio = Folio.objects.get_next_folio('INCIDENCIAS', user.sucursal.id)
    incidencia.folio = folio
    incidencia.embarque = entrega.embarque.documento
    ####### Informacion Entrega
    incidencia.sucursal = entrega.sucursal
    incidencia.destinatario = entrega.destinatario
    incidencia.operador = entrega.operador
    incidencia.origen = entrega.origen
    incidencia.entidad = entrega.entidad
    incidencia.realizo = entrega.realizo
    incidencia.fecha_documento = entrega.fecha_documento
    incidencia.documento = entrega.documento
    incidencia.tipo_documento = entrega.tipo_documento
    ###### Informacion EntregaDet
    incidencia.clave = entrega_det.clave
    incidencia.descripcion = entrega_det.descripcion
    incidencia.cantidad =  entrega_det.cantidad
    incidencia.valor = entrega_det.valor
    incidencia.fecha = datetime.today()
    ######## Infomacion Incidencia
    incidencia.motivo = incidencia_dict['motivo']
    incidencia.comentario = incidencia_dict['comentario']
    if "devuelto" in incidencia_dict:
        incidencia.devuelto = incidencia_dict['devuelto']
    if "entregado" in incidencia_dict:
        incidencia.entregado = incidencia_dict['entregado']
    if "incompleto" in incidencia_dict:
        incidencia.incompleto = incidencia_dict['incompleto']
    if "maltratado" in incidencia_dict:
        incidencia.maltratado = incidencia_dict['maltratado']
    if "impreso" in incidencia_dict:
        incidencia.impreso = incidencia_dict['impreso']
    if "cortado" in incidencia_dict:
        incidencia.cortado = incidencia_dict['cortado'] 
    if "img1" in incidencia_dict:
        incidencia.img1 = incidencia_dict['img1']
    if "img2" in incidencia_dict:
        incidencia.img2 = incidencia_dict['img2']
    if "img3" in incidencia_dict:
        incidencia.img3 = incidencia_dict['img3']
    incidencia.save()
    Folio.objects.set_folio('INCIDENCIAS', user.sucursal.id)
    return entrega_det
   

def get_user_logged(request):
    authentication = JWTAuthentication()
    header = authentication.get_header(request)
    raw_token = authentication.get_raw_token(header) 
    validated_token = authentication.get_validated_token(raw_token)
    user = authentication.get_user(validated_token)
    return user
    
