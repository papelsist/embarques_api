from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse
from ..models import Envio,EnvioDet, Entrega
from ..serializers import EnvioSerializer


@api_view(['GET'])
def pendientes_envio(request):
    print("Ejecutando el TEST de Envio")
    envios = Envio.objects.pendientes_envio()
    envios_serialized = EnvioSerializer(envios, many= True)
    return Response(envios_serialized.data) 

@api_view(['GET'])
def transito_envio(request):
    print("Ejecutando el tablero de transito ")
    transito = Entrega.objects.all()

    return Response({"Test": "Completado"})

