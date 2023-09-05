from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView, 
                                    CreateAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    UpdateAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveUpdateDestroyAPIView)
from ..models import Operador
from ..serializers import OperadorSerializer
from ..models import  Operador

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
    serializer_class = OperadorSerializer
    def get_queryset(self):
        print(self.request.query_params.get('term'))
        term = self.request.query_params.get('term')
        founds = Operador.objects.find_operador(term)
        return   founds
    