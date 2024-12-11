from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from datetime import date, datetime
from applications.authentication.models import User
from ..serializers import PreEntregaSerializer,EnvioSerializerEm
from ..models import PreEntrega, PreEntregaDet, Envio, EnvioDet
from rest_framework.generics import (ListAPIView, 
                                    CreateAPIView,
                                    RetrieveAPIView,
                                    RetrieveUpdateAPIView
                                    )



class PreEntregaSurtidoListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PreEntregaSerializer
    def get_queryset(self):
        print(self.request.query_params)
        sucursal = self.request.query_params.get('sucursal')
        queryset = PreEntrega.objects.filter(sucursal=sucursal, surtido = None).order_by('folio')
        return queryset
    

class EnviosSurtidoListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        print(self.request.query_params)
        sucursal = self.request.query_params.get('sucursal')
        envios = Envio.objects.filter(sucursal=sucursal, surtido = None).order_by('date_created')
        queryset = [x for x in envios if x.enviado == 0.00]
        return queryset
        
    
@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_surtido_preentrega(request):
    data = request.data
    preentrega = PreEntrega.objects.get(pk=data['preentrega_id'])

    for pd in data['detalles']:
        preentrega_det = PreEntregaDet.objects.get(pk=pd)
        preentrega_det.surtido = datetime.now()
        preentrega_det.surtidor = data['surtidor']
        preentrega_det.save()

    surtidos = preentrega.detalles.filter(surtido__isnull=False).count()
    partidas = preentrega.detalles.count()

    if surtidos == partidas:
        preentrega.surtido = datetime.now()
        preentrega.save()
    
    preentrega_serialized = PreEntregaSerializer(preentrega)

    return Response(preentrega_serialized.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_surtido_envio(request):
    data = request.data
    print(data)

    envio = Envio.objects.get(pk=data['envio_id'])

    for ed in data['detalles']:
        envio_det = EnvioDet.objects.get(pk=ed)
        envio_det.surtido = datetime.now()
        envio_det.surtidor = data['surtidor']
        envio_det.save()

    surtidos = envio.detalles.filter(surtido__isnull=False).count()
    partidas = envio.detalles.count()

    if surtidos == partidas:
        envio.surtido = datetime.now()
        envio.save()

    envio_serialized = EnvioSerializerEm(envio)

    return Response(envio_serialized.data)