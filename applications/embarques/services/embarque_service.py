from ..models import Embarque,Entrega,EntregaDet,Envio,EnvioDet, EntregaIncidencia, ImgEntrega, Folio, Operador, Sucursal, PreEntrega, PreEntregaDet, DireccionEntrega
from django.db.models import Q, Sum, DecimalField, Prefetch
from django.db.models.functions import Coalesce
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime, date
from decimal import Decimal
from applications.localizacion_gps.services import get_ubicacion



def salvar_embarque(embarque_dict):
    """ Funcion para actualizar un embarque despues de haberlo creado 

    Args:
        embarque_dict (_type_): _description_
    """

    print("Salvando y actualizando embarque")
 
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
        for det in ent['detalles']:
            envio_det = EnvioDet.objects.get(id = det['id'])
            enviar = Decimal(det['enviar'])
            
            kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
            valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))

            try:
                entrega_det = EntregaDet.objects.get(id = det['entregaDetId'])
                entrega_det.cantidad = det['enviar']
                entrega_det.kilos = kilos_envio
                entrega_det.valor = valor_envio
            except EntregaDet.DoesNotExist as e:
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
           
        entrega.kilos = kilos_entrega
        entrega.valor = valor_entrega

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
                try:
                    instruccion = PreEntrega.objects.get(entrega = entrega)
                    instruccion.entrega = None
                    instruccion.save()
                except PreEntrega.DoesNotExist as e:
                    pass
                entrega.delete()
            else:
                kilos_entrega = 0
                valor_entrega = 0
                for det in detalles:
                    kilos_entrega += det.kilos
                    valor_entrega += det.valor
                entrega.kilos = kilos_entrega
                entrega.valor = valor_entrega
                
        return entrega_det_deleted[0] 
    else: 
        return 0
    

def registrar_salida_embarque(embarque_dict):
    embarque = Embarque.objects.get(id = embarque_dict['id'])
    embarque.or_fecha_hora_salida = datetime.now()
    for partida in embarque.partidas.all():
        partida.salida = datetime.now()
        if partida.envio.pagado:
            partida.recepcion_pago = datetime.now()
        partida.save()   
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

    prefetch_partidas = Prefetch('partidas', queryset=Entrega.objects.prefetch_related('detalles').all())
    embarque = Embarque.objects.select_related('operador','operador__transporte').prefetch_related(prefetch_partidas).get(id = embarque_dict['id'])
    partidas_dict = embarque_dict['partidas']
    entregas_list = embarque.partidas.all()
    for partida in partidas_dict:
        #entrega = Entrega.objects.get(id = partida['entregaId'])
        #entrega = entregas_list.(id = partida['entregaId'])
        entrega = next(filter(lambda e: e.id == partida['entregaId'], entregas_list), None)
        print("Actualizando entrega id: ", entrega)
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
       
        if entrega.arribo_latitud == None or entrega.recepcion_latitud == None:
            transporte = entrega.embarque.operador.transporte
            try:
                ubicacion = get_ubicacion(transporte.imei)
                if entrega.arribo and  entrega.arribo_latitud == None:
                    entrega.arribo_latitud = ubicacion['latitude']
                    entrega.arribo_longitud = ubicacion['longitude']
                    entrega.save()

                if entrega.recepcion and  entrega.recepcion_latitud == None:
                    entrega.recepcion_latitud = ubicacion['latitude']
                    entrega.recepcion_longitud = ubicacion['longitude']
                    entrega.save()
            except Exception as e:
                print("El operdor no tiene imei asignado")
                print(e)

    return embarque


def registrar_recepcion_pagos_embarque(embarque_dict):
    embarque = Embarque.objects.get(id = embarque_dict['id'])
    for id in embarque_dict['partidas']:
        entrega = Entrega.objects.get(id = id)
        if entrega.recepcion != None:
            entrega.recepcion_pago = datetime.now()
            entrega.save()
    return embarque


def registrar_recepcion_docs_embarque(embarque_dict):
    embarque = Embarque.objects.get(id = embarque_dict['id'])
    for id in embarque_dict['partidas']:
        entrega = Entrega.objects.get(id = id)
        if entrega.recepcion != None:
            entrega.recepcion_documentos = datetime.now()
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

    partidas = embarque.partidas.all().filter((Q(recepcion = None) | Q(recepcion_documentos = None)  | (Q(tipo_documento = 'COD') & Q(recepcion_pago = None ))))
    mensaje = ""
    if len(partidas) == 0:
        embarque.regreso=  datetime.now()
        embarque.save()
        for partida in embarque.partidas.all():
            partida.regreso = datetime.now()
            partida.save()
        actualizado = 1
        mensaje = "Embarque actualizado"
    else:
        actualizado = 0
        recepciones = embarque.partidas.all().filter(recepcion = None)
        documentos = embarque.partidas.all().filter(recepcion_documentos = None)
        pagos = embarque.partidas.all().filter(tipo_documento = 'COD').filter(recepcion_pago = None)
        if len(recepciones) != 0:
            mensaje = "Faltan recepciones"
            return embarque, actualizado, mensaje 
        if len(documentos) != 0:
            mensaje = "Faltan recepcion de documentos"
            return embarque, actualizado, mensaje 
        if len(pagos) != 0:
            mensaje = "Faltan recepcion de pagos"
            return embarque, actualizado, mensaje 

    return embarque, actualizado, mensaje 


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


def asignar_envios_pend(data):
    print(data)
    embarque = Embarque.objects.select_related('operador','sucursal').get(pk=data['embarque_id'])
    kilos_embarque = 0
    for env in data['envios']:
        detalles_prefetch = Prefetch('detalles', queryset=EnvioDet.objects.all())
        envio = Envio.objects.prefetch_related(detalles_prefetch).get(pk=env)
        #Se crea la entrega
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
        #Agregar partidas
        for det in envio.detalles.all():
            if det.clave != 'CORTE':
                envio_det = EnvioDet.objects.get(pk = det.id)
                total_entregado = envio_det.entregas.all().aggregate(
                    total_entregado = Coalesce(Sum('cantidad'), 0, output_field=DecimalField())
                )
                enviar = Decimal(det.me_cantidad)
                kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
                valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))
                entrega_det = EntregaDet(
                        entrega= entrega,
                        envio_det = det,
                        clave = det.clave,
                        descripcion = det.me_descripcion,
                        cantidad = det.me_cantidad - total_entregado['total_entregado'],
                        valor = valor_envio,
                        kilos = kilos_envio
                    )
                entrega_det.save()
                kilos_entrega += kilos_envio
                valor_entrega += valor_envio
        entrega.kilos = kilos_entrega
        entrega.valor = valor_entrega
        entrega.save()
        kilos_embarque += kilos_entrega
    embarque.kilos = kilos_embarque
    embarque.save()


def asignar_envios_parc(data):
    print(data)
    embarque = Embarque.objects.get(pk=data['embarque_id'])
    envio = Envio.objects.get(pk=data['envio_id'])

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

    for det in  data['detalles']:
        print("*"*50)
        print(det)
        envio_det = EnvioDet.objects.get(pk = det['id'])
        enviar = Decimal(det['enviar'])
        kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
        valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))
        entrega_det = EntregaDet(
                entrega= entrega,
                envio_det = envio_det,
                clave = det['clave'],
                descripcion = det['me_descripcion'],
                cantidad = enviar,
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
    embarque.kilos = kilos_entrega
    embarque.save()

    return None


def asignar_a_pasan(data):
    print(data)
    comentario = data['comentario']
    operador = Operador.objects.get(nombre = 'CLIENTE PASAN')
    envio = Envio.objects.get(pk=data['envio_id'])
    sucursal = Sucursal.objects.get(nombre = envio.sucursal)
    folio = Folio.objects.get_next_folio('EMBARQUES_PASAN',sucursal.id)
    fecha = date.today()
    or_fecha_hora_salida = datetime.now()
    regreso = datetime.now()
    embarque = Embarque.objects.create(
        documento = folio, 
        operador = operador,
        sucursal = sucursal,
        facturista= operador.facturista,
        fecha = fecha, 
        comentario = comentario, 
        version = 0,
        or_fecha_hora_salida = or_fecha_hora_salida,
        regreso = regreso
        )
    Folio.objects.set_next_folio('EMBARQUES_PASAN', folio,sucursal.id)
    
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
        origen = envio.tipo_documento,
        arribo = datetime.now(),
        recepcion = datetime.now(),
        recibio = 'CLIENTE PASAN'
    )
    entrega.save()
    kilos_entrega = 0
    valor_entrega = 0

    for det in  data['detalles']:
        print("*"*50)
        print(det)
        envio_det = EnvioDet.objects.get(pk = det['id'])
        enviar = Decimal(det['enviar'])
        kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
        valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))
        entrega_det = EntregaDet(
                entrega= entrega,
                envio_det = envio_det,
                clave = det['clave'],
                descripcion = det['me_descripcion'],
                cantidad = enviar,
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
    embarque.kilos = kilos_entrega
    embarque.save()

    return None


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
    
def crear_pre_entrega (data):

    print(f"Data: {data}")
    comentario = data['comentario']
    fecha_entrega = data['fecha_entrega']
    envio = Envio.objects.get(pk=data['envio_id'])
    sucursal = Sucursal.objects.get(nombre = envio.sucursal)
    folio = Folio.objects.get_next_folio('PREENTREGA',sucursal.id)
    direccion_entrega = DireccionEntrega.objects.get(pk = data['direccion_entrega_id'])

    preentrega = PreEntrega()
    preentrega.envio = envio
    preentrega.fecha = date.today()
    preentrega.sucursal = sucursal.nombre
    preentrega.folio = folio
    preentrega.comentario = comentario
    preentrega.destinatario = envio.destinatario
    preentrega.documento = envio.documento
    preentrega.tipo_documento = envio.tipo_documento
    preentrega.fecha_documento = envio.fecha_documento
    preentrega.direccion_entrega = direccion_entrega
    preentrega.fecha_entrega = fecha_entrega

    preentrega.save()

    for det in  data['detalles']:
        envio_det = EnvioDet.objects.get(pk = det['id'])
        preentrega_det = PreEntregaDet()
        preentrega_det.preentrega = preentrega
        preentrega_det.envio_det = envio_det
        preentrega_det.cantidad = det['cantidad']
        preentrega_det.clave = envio_det.clave
        preentrega_det.descripcion = envio_det.me_descripcion
        preentrega_det.cortes = envio_det.cortes

        preentrega_det.save()

    Folio.objects.set_next_folio('PREENTREGA', folio,sucursal.id)
    
  
    return None


def asignar_instruccion(data):
    print(f"Data: {data}")

    instruccion = PreEntrega.objects.get(pk=data['id'])
    embarque = Embarque.objects.get(pk=data['embarque_id'])
    envio = instruccion.envio
    print(f"Instruccion: {instruccion}")
    print(f"Embarque: {embarque}")

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
    
    for det in instruccion.detalles.all():
        envio_det = det.envio_det
        print(envio_det)
        enviar = det.cantidad
        kilos_envio = ((envio_det.me_kilos * enviar )/envio_det.me_cantidad)
        valor_envio = Decimal(((envio_det.valor * enviar )/envio_det.me_cantidad))
        entrega_det = EntregaDet(
                entrega= entrega,
                envio_det = envio_det,
                clave = det.clave,
                descripcion = det.descripcion,
                cantidad = enviar,
                valor = valor_envio,
                kilos = kilos_envio
            )
        entrega_det.save()
        kilos_entrega += kilos_envio
        valor_entrega += valor_envio
       
    entrega.kilos = kilos_entrega
    entrega.valor = valor_entrega
    print("Entrega kilos: ", entrega.kilos)
    entrega.save() 
    embarque.kilos = kilos_entrega
    embarque.save()
    instruccion.entrega = entrega
    instruccion.save()


    return None
