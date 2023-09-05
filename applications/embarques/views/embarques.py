from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from ..models import Envio, Entrega,Embarque,Folio, Operador, Sucursal,FacturistaEmbarques
from ..serializers import EnvioSerializerEm, EntregaSerializer, EmbarqueSerializer

from rest_framework.generics import (ListAPIView, 
                                    CreateAPIView,
                                    RetrieveAPIView,
                                    RetrieveUpdateAPIView
                                    )
from ..services import salvar_embarque






@api_view(['GET'])
def facturas_transito(request):
    entrega = Entrega.objects.all()
    entrega_serialized = EntregaSerializer(entrega, many=True)
    return Response({'Test':'Completo','data':entrega_serialized.data})


@api_view(['GET'])
def search_envio(request):
    documento = request.query_params.get('documento')
    tipo = request.query_params.get('tipo')
    fecha_documento = request.query_params.get('fecha_documento')
    try:
        envio = Envio.objects.find_envio(tipo, documento, fecha_documento)
        envio_serialized = EnvioSerializerEm(envio)
        data = envio_serialized.data
    except:
        data = None
    return Response(data)

@api_view(['POST'])
def crear_embarque(request):
    folio = Folio.objects.get_next_folio('EMBARQUES')
    operador_id =request.data['operador']
    sucursal_id = request.data['sucursal']
    facturista_id = request.data['facturista']
    fecha = date.today()
    operador = Operador.objects.get(id=operador_id)
    sucursal = Sucursal.objects.get(id = sucursal_id)
    facturista = FacturistaEmbarques.objects.get(id = facturista_id)
    comentario = request.data.get('comentario')
    embarque = Embarque.objects.create(documento = folio, operador = operador,sucursal = sucursal,facturista= facturista,fecha = fecha, comentario = comentario, version = 0)
    embarque_serialized = EmbarqueSerializer(embarque)
    Folio.objects.set_next_folio('EMBARQUES', folio)
    return Response(embarque_serialized.data)


class CrearAsignacion(RetrieveAPIView):
    serializer_class = EmbarqueSerializer
    queryset = Embarque.objects.filter()
    
@api_view(['POST'])
def actualizar_embarque(request):
    salvar_embarque(request.data)
    return Response({"message":"Complete sucesfully" })



class PendientesSalida(ListAPIView):
    serializer_class = EmbarqueSerializer
    queryset = Embarque.objects.pendientes_salida()




''' @api_view(['GET'])
def pendientes_salida(request):
     embarques = Embarque.objects.pendientes_salida()
     embarques_serialized = EmbarqueSerializer(embarques, many= True)
     return Response(embarques_serialized.data) '''
  
    
   
