from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from datetime import date
from applications.authentication.models import User
from ..models import Envio, Entrega,EntregaDet,Embarque,Folio, Operador, Sucursal,FacturistaEmbarques, Operador, EntregaIncidencia, EntregaIncidenciaSeguimiento, InstruccionDeEnvio
from ..serializers import EnvioSerializerEm, EntregaSerializer, EmbarqueSerializer, IncidenciaSerializer,EmbarqueRutaSerializer,EntregaRutaSerializer,SucursalSerializer, IncidenciaSeguimientoSerializer
from rest_framework.generics import (ListAPIView, 
                                    CreateAPIView,
                                    RetrieveAPIView,
                                    RetrieveUpdateAPIView
                                    )
from ..services import (salvar_embarque, borrar_entrega_det, registrar_salida_embarque, borrar_embarque, actualizar_bitacora_embarque, 
                        eliminar_entrega_embarque, registrar_regreso_embarque, crear_embarque_por_ruteo, asignar_envios_pend, get_user_logged,
                        crear_incidencia_entrega_det, asignar_envios_parc, asignar_a_pasan)

from geopy import distance
from datetime import date



class PendientesSalida(ListAPIView):

    serializer_class = EmbarqueSerializer
   
    def get_queryset(self):
        suc_id = self.request.query_params['sucursal']
        sucursal = Sucursal.objects.get(id = suc_id) 
        queryset = Embarque.objects.pendientes_salida(sucursal)
        return queryset
        

@api_view(['POST'])
def crear_embarque(request):

    operador_id =request.data['operador']
    sucursal_id = request.data['sucursal']
    folio = Folio.objects.get_next_folio('EMBARQUES',sucursal_id)
    facturista_id = request.data['facturista']
    fecha = date.today()
    operador = Operador.objects.get(id=operador_id)
    sucursal = Sucursal.objects.get(id = sucursal_id)
    facturista = FacturistaEmbarques.objects.get(id = facturista_id)
    comentario = request.data.get('comentario')
    embarque = Embarque.objects.create(documento = folio, operador = operador,sucursal = sucursal,facturista= facturista,fecha = fecha, comentario = comentario, version = 0)
    embarque_serialized = EmbarqueSerializer(embarque)
    Folio.objects.set_next_folio('EMBARQUES', folio,sucursal_id)
    return Response(embarque_serialized.data)

@api_view(['GET'])
def search_envio(request):
    sucursal = request.query_params.get('sucursal')
    documento = request.query_params.get('documento')
    tipo = request.query_params.get('tipo')
    fecha_documento = request.query_params.get('fecha_documento')
    try:
        envio = Envio.objects.find_envio(tipo, documento, fecha_documento,sucursal)
        envio_serialized = EnvioSerializerEm(envio)
        data = envio_serialized.data
    except:
        data = None
    return Response(data)


class GetEnvio(RetrieveAPIView):
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        print("Get Envio")
        print(self)
    
        queryset = Envio.objects.filter()
        return queryset
    

class CrearAsignacion(RetrieveAPIView):
    serializer_class = EmbarqueSerializer
    queryset = Embarque.objects.filter()


@api_view(['POST'])
def actualizar_embarque(request):
    salvar_embarque(request.data)
    return Response({"message":"Complete sucesfully" })


@api_view(['POST'])
def eliminar_entrega_det(request):  
    deleted = borrar_entrega_det(request.data)
    return Response({"deleted": deleted })

@api_view(['POST'])
def registrar_salida(request):
    embarque = registrar_salida_embarque(request.data)
    embarque_serialized = EmbarqueSerializer(embarque)
    return Response(embarque_serialized.data)

@api_view(['POST'])
def eliminar_embarque(request):
    print(request.data)
    deleted = borrar_embarque(request.data)
    return Response({"deleted": deleted })

class Transito(ListAPIView):
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        queryset = Embarque.objects.transito(sucursal)
        return queryset
   

class ActualizarEntregas(RetrieveAPIView):
    serializer_class = EmbarqueSerializer
    queryset = Embarque.objects.filter()


@api_view(['POST'])
def actualizar_bitacora(request):

    embarque = actualizar_bitacora_embarque(request.data)
    embarque_serialized = EmbarqueSerializer(embarque)
    return Response(embarque_serialized.data)

@api_view(['POST'])
def eliminar_entrega(request):
  
    deleted = eliminar_entrega_embarque(request.data)
    return Response({"deleted": deleted })

@api_view(['POST'])
def registrar_regreso(request):
    embarque, actualizado = registrar_regreso_embarque(request.data)
    embarque_serialized = EmbarqueSerializer(embarque)
    return Response({"embarque":embarque_serialized.data, "actualizado": actualizado})

class Regresos(ListAPIView):
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        queryset = Embarque.objects.regresos(fecha_inicial,fecha_final,sucursal)
        return queryset
    
class EmbarquesPasan(ListAPIView):
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        queryset = Embarque.objects.embarques_pasan(fecha_inicial,fecha_final,sucursal)
        return queryset


class EnviosPendientes(ListAPIView):
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        print (self.request.query_params)
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        sucursal = self.request.query_params.get('sucursal')
        envios = Envio.objects.pendientes_salida(fecha_inicial, fecha_final, sucursal)
        
        return envios
    
class EnviosParciales(ListAPIView):
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        sucursal = self.request.query_params.get('sucursal')
        envios = Envio.objects.envios_parciales(fecha_inicial, fecha_final, sucursal)
        return envios
    
@api_view(['POST'])
def embarque_por_ruteo(request):
    ruta = request.data
    embarque = crear_embarque_por_ruteo(ruta)
    return Response({})

@api_view(['POST'])
def asignar_envios_pendientes(request):
    data = request.data
    asignar_envios_pend(data)
    return Response({})

@api_view(['POST'])
def asignar_envios_parciales(request):
    data = request.data
    asignar_envios_parc(data)
    return Response({})

class TransitoOperador(ListAPIView):
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        user = get_user_logged(self.request)
        print(user)
        operador = Operador.objects.get(user = user)
        queryset = Embarque.objects.transito_operador(operador)
        return queryset
    
class RegresosOperador(ListAPIView):
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        user = get_user_logged(self.request)
        print(user)
        operador = Operador.objects.get(user = user)
        queryset = Embarque.objects.regresos_operador(fecha_inicial,fecha_final,operador)
        return queryset
    

@api_view(['POST'])
def crear_incidencia_entrega(request):
    data = request.data
    entrega_det_id= data['entrega_det']
    entrega_det = crear_incidencia_entrega_det( entrega_det_id,data['incidencia'],request)
    #print(entrega_det)
 
    return Response({"message":"Complete sucesfully"})

    
class RutaEmbarque(RetrieveAPIView):
    serializer_class = EmbarqueRutaSerializer
    queryset = Embarque.objects.filter()

class EntregaRuta(RetrieveAPIView):
    serializer_class = EntregaRutaSerializer
    queryset = Entrega.objects.filter()

class IncidenciasEntrega(ListAPIView):
    serializer_class = IncidenciaSerializer
    def get_queryset(self):
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')
        queryset = EntregaIncidencia.objects.incidencias_periodo(fecha_inicial,fecha_final)
        return queryset
    
class Incidencia(RetrieveAPIView):
    serializer_class = IncidenciaSerializer
    queryset = EntregaIncidencia.objects.filter()   

@api_view(['POST'])
def crear_seguimiento(request):

    authentication = JWTAuthentication()
    header = authentication.get_header(request)
    raw_token = authentication.get_raw_token(header) 
    validated_token = authentication.get_validated_token(raw_token)
    user = authentication.get_user(validated_token)

    data = request.data
    incidencia_id = data['incidencia']
    incidencia = EntregaIncidencia.objects.get(id = incidencia_id)
    seguimiento = EntregaIncidenciaSeguimiento.objects.create(incidencia = incidencia,comentario = data['comentario'],create_user = user.username,update_user = user.username,fecha = date.today())
    seguimiento_serialized = IncidenciaSeguimientoSerializer(seguimiento)
    return Response(seguimiento_serialized.data)
    
  

@api_view(['GET'])  
def test_view(request):
    print(request)
    return Response({"Message":"Test"})

@api_view(['GET'])
def validar_cercania(request):
    print(request.query_params)
    print(request.query_params['latitud'])
    print(type(request.query_params['latitud']))
    print(request.query_params['longitud'])
    print(type(request.query_params['longitud']))

    transporte_ubicacion = (request.query_params['latitud'],request.query_params['longitud'])
    sucursales = Sucursal.objects.all()
    for sucursal in sucursales:
        sucursal_ubicacion = (sucursal.direccion_latitud,sucursal.direccion_longitud)
        distancia = distance.distance(transporte_ubicacion,sucursal_ubicacion).km
        if distancia < .1:
            print(sucursal.nombre)
            sucursal_serialized = SucursalSerializer(sucursal)
            return Response(sucursal_serialized.data)
        print(distancia)

    return Response({"Message":"Sin sucursal cercana"})

@api_view(['POST'])
def crear_embarque_operador(request):

    user_id =request.data['usuario']
    sucursal_id = request.data['sucursal']
    folio = Folio.objects.get_next_folio('EMBARQUES',sucursal_id)
    #facturista_id = request.data['facturista']
    fecha = date.today()
    user = User.objects.get(id=user_id)
    operador = user.operador.first()
    sucursal = Sucursal.objects.get(id = sucursal_id)
    facturista = FacturistaEmbarques.objects.get(id = operador.facturista.id)
    comentario = request.data.get('comentario')
    print(operador.nombre)
    print(sucursal.nombre)
    print(facturista.nombre)
    embarque = Embarque.objects.create(documento = folio, operador = operador,sucursal = sucursal,facturista= facturista,fecha = fecha, comentario = comentario, version = 0)
    embarque_serialized = EmbarqueSerializer(embarque)
    Folio.objects.set_next_folio('EMBARQUES', folio,sucursal_id)
    return Response(embarque_serialized.data)

@api_view(['POST'])
def actualizar_fecha_entrega(request):
    print(request.data)
    envio_id = request.data['envio_id']
    fecha_entrega = request.data['fecha_entrega']
    envio = Envio.objects.get(id = envio_id)
    instruccion = InstruccionDeEnvio.objects.get(envio = envio)
    instruccion.fecha_de_entrega = fecha_entrega
    instruccion.save()
    envio_serialized= EnvioSerializerEm(envio)
    return Response(envio_serialized.data)
    
@api_view(['POST'])
def actualizar_pasan_total(request):
    print(request.data)
    envio_id = request.data['envio_id']
    envio = Envio.objects.get(id = envio_id)
    user = get_user_logged(request)
    envio.pasan = True
    envio.usuario_pasan = "Pruebas"
    envio.save()
    envio_serialized= EnvioSerializerEm(envio)
    return Response(envio_serialized.data)

@api_view(['POST'])
def asignar_pasan(request):
    envio = asignar_a_pasan(request.data)
    envio_serialized= EnvioSerializerEm(envio)
    return Response(envio_serialized.data)

@api_view(['GET'])
def search_entrega_mtto(request):
  
    sucursal = request.query_params.get('sucursal')
    documento = request.query_params.get('documento')
    embarque = request.query_params.get('embarque')
    print(request.query_params)
    #try:
    entrega = Entrega.objects.filter( sucursal = sucursal,documento = documento,embarque__documento = embarque, embarque__regreso = None).first()
    message = "Entrega encontrada"
    if entrega == None:
        message = "Entrega no encontrada"
        
    entrega_serialized = EntregaSerializer(entrega)
    data = entrega_serialized.data
    ##except:
    #    data = None
    return Response({"data":data, "message":message}) 


@api_view(['PUT'])
def actualizar_bitacora_entrega(request):
    entrega = Entrega.objects.get(id = request.data['entrega_id'])
    cancelar_arribo = request.data.get('cancelar_arribo')
    cancelar_recepcion = request.data.get('cancelar_recepcion')

    if entrega.embarque.regreso == None:

        if  entrega.recepcion != None and cancelar_recepcion:
            entrega.recepcion = None
            entrega.recepcion_latitud = None
            entrega.recepcion_longitud = None
            entrega.recibio = None

        if  entrega.recepcion  == None and entrega.arribo != None and cancelar_arribo:
            entrega.arribo = None
            entrega.arribo_latitud = None
            entrega.arribo_longitud = None
         

        entrega.save()

        entrega_serialized = EntregaSerializer(entrega)
        return Response({"data":entrega_serialized.data, "message":"Actualizado correctamente"})
    
    entrega_serialized = EntregaSerializer(entrega)
    return Response({"data":entrega_serialized.data, "message":"No se puede actualizar la bitacora de una entrega con regreso"})



