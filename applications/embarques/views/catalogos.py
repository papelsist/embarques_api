from django.shortcuts import render
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView, 
                                    CreateAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    UpdateAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveUpdateDestroyAPIView)
from ..serializers import OperadorSerializer, SucursalSerializer
from ..models import  Operador, Sucursal
from applications.core.models import Cliente
from applications.core.serializers import ClienteSerializer

class OperadorList(ListAPIView):
    queryset = Operador.objects.all()
    serializer_class = OperadorSerializer

class OperadorCreate(CreateAPIView):
    serializer_class = OperadorSerializer

class OperadorRetrieve(RetrieveAPIView):
    serializer_class = OperadorSerializer
    queryset = Operador.objects.filter()

class OperadorDelete(DestroyAPIView):
    serializer_class = OperadorSerializer
    queryset = Operador.objects.filter()

class OperadorUpdate(UpdateAPIView):
    serializer_class = OperadorSerializer
    queryset = Operador.objects.filter()

class OperadorGetUpdate(RetrieveUpdateAPIView):
    serializer_class = OperadorSerializer
    queryset = Operador.objects.filter()

class OperadorGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = OperadorSerializer
    queryset = Operador.objects.filter()

class SearchOperador(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = OperadorSerializer
    def get_queryset(self):
        print(self.request.query_params.get('term'))
        term = self.request.query_params.get('term')
        founds = Operador.objects.find_operador(term)
        return   founds


class SearchCliente(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClienteSerializer

    def get_queryset(self):
        term = (self.request.query_params.get('term') or '').strip()
        if len(term) < 2:
            return Cliente.objects.none()
        return Cliente.objects.filter(
            Q(nombre__icontains=term)
            | Q(clave__icontains=term)
            | Q(rfc__icontains=term)
            | Q(razon_social__icontains=term),
            activo=True,
        ).order_by('nombre')[:30]


class SucursalList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer


class SucursalesActivasList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Sucursal.objects.filter(activa=True)
    serializer_class = SucursalSerializer
