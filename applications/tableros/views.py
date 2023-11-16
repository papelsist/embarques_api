from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from applications.embarques.serializers import EnvioSerializerEm, EmbarqueSerializer
from applications.embarques.models import Envio, Sucursal, Embarque
from rest_framework.generics import (ListAPIView)



class EnviosPendientesAsignacion(ListAPIView):
    serializer_class = EnvioSerializerEm
    def get_queryset(self):
        sucursal = self.request.query_params.get('sucursal')
        envios = Envio.objects.pendientes_asignacion(sucursal)
        envios_ser = [env for env in envios if env.saldo > 0  ]
        return envios_ser
    


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
        queryset = Embarque.objects.transito(sucursal)
        return queryset