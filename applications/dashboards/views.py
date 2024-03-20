from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from applications.embarques.models import Embarque
from applications.embarques.serializers import EmbarqueOperadorSerializer

# Create your views here.


@api_view(['GET']) 
def embarques_operador(request):
    fecha_inicial = request.GET.get('fecha_inicial')
    fecha_final = request.GET.get('fecha_final')
    print(fecha_inicial, fecha_final)
    embarques = Embarque.objects.embarques_operador_kilos(fecha_inicial, fecha_final)
    embarques_serialized = EmbarqueOperadorSerializer(embarques, many=True)
    return Response(embarques_serialized.data)