from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from ..models import Envio,EnvioDet, EntregaParcial
from ..serializers import EnvioSerializer


@api_view(['GET'])
def pendientes_envio(request):
    print("Ejecutando el TEST de Envio")
    envios = Envio.objects.pendientes_envio()
    for envio in envios:
        print("*"*50)
        print(envio.__dict__)
    envios_serialized = EnvioSerializer(envios, many= True)

    return Response({'Test':'Completo',"data": envios_serialized.data}) 