from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from applications.embarques.serializers import EnvioSerializerEm, EmbarqueSerializer, EnvioSerializer, EntregaSerializer
from applications.embarques.models import Envio, Sucursal, Embarque, Entrega   
from rest_framework.generics import (ListAPIView)



class EnviosPendientesAsignacion(ListAPIView):
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        sucursal = self.request.query_params.get('sucursal')
        envios = Envio.objects.pendientes_asignacion(sucursal)
        return envios
    


class EmbarquesPendientesSalida(ListAPIView):
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        suc_id = self.request.query_params['sucursal']
        sucursal = Sucursal.objects.get(id = suc_id) 
        queryset = Embarque.objects.pendientes_salida(sucursal)
        return queryset
        
class EmbarquesTransito(ListAPIView):
    serializer_class = EmbarqueSerializer
    def get_queryset(self):
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        queryset = Embarque.objects.transito(sucursal).order_by('or_fecha_hora_salida')
        return queryset
    
class EnviosTransito(ListAPIView):
    serializer_class = EntregaSerializer
    def get_queryset(self):
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        query_set = Entrega.objects.filter(recepcion = None, embarque__sucursal = sucursal).order_by('salida')
        return query_set
    
class EnviosParciales(ListAPIView):
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        suc_id = self.request.query_params.get('sucursal')
        sucursal = Sucursal.objects.get(id = suc_id)
        query_set =  Envio.objects.envios_parciales_pendientes(sucursal)
        return query_set

        
    
