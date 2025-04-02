from django.shortcuts import render
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from applications.embarques.serializers import EnvioSerializerEm, EmbarqueSerializer, EnvioSerializer, EntregaSerializer, ImgEntregaSerializer
from applications.embarques.models import Envio, Sucursal, Embarque, Entrega, ImgEntrega  
from rest_framework.generics import (ListAPIView)
from datetime import date, timedelta



class Regresos(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        fecha_final = date.today()
        fecha_inicial = fecha_final - timedelta(days=7)    
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        queryset = Embarque.objects.regresos(fecha_inicial,fecha_final,sucursal)
        return queryset

class EnviosPendientesAsignacion(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        sucursal = self.request.query_params.get('sucursal')
        envios = Envio.objects.pendientes_asignacion(sucursal)
        return envios
    


class EmbarquesPendientesSalida(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        suc_id = self.request.query_params['sucursal']
        sucursal = Sucursal.objects.get(id = suc_id) 
        queryset = Embarque.objects.pendientes_salida(sucursal)
        return queryset
        
class EmbarquesTransito(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        queryset = Embarque.objects.transito(sucursal).order_by('or_fecha_hora_salida')
        return queryset
    
class EnviosTransito(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EntregaSerializer
    def get_queryset(self):
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        query_set = Entrega.objects.filter(~Q(embarque__or_fecha_hora_salida = None),recepcion = None, embarque__sucursal = sucursal).order_by('salida')
        return query_set
    
class EnviosParciales(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        query_set =  Envio.objects.envios_parciales_pendientes(sucursal)
        return query_set

class CapturasEntregas(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ImgEntregaSerializer
    def get_queryset(self):
        print(self.request.query_params)
        fecha = self.request.query_params.get('fecha')  
        sucursal = self.request.query_params.get('sucursal')
        query_set = ImgEntrega.objects.filter(entrega__sucursal = sucursal, entrega__embarque__fecha = fecha).order_by('-id')
        return query_set

      


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def whatsapp(request):

    print(request.query_params)
    print(request.data)
    if 'hub.challenge' in request.query_params:
        challenge = int(request.query_params.get('hub.challenge'))
        print(challenge)

        return Response(challenge)
    
    return Response('ok')