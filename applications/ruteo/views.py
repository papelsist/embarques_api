from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse,  JsonResponse

from .services.ruteo import build_ruteo_by_pendientes, build_ruteo_by_envios, ruteo_dj_orm
from .services.optimizacion_rutas import optimizacion_ruta_embarque
from .serializers import RutasSerializer

# Create your views here.


#818,817,816,2430,832,825,2270,361

@api_view(['GET'])
def sugerencia_ruta_pendientes(request):
    fecha = request.query_params['fecha']
    sucursal = request.query_params['sucursal']
    '''  print("*"*50)
    print(sucursal)
    print("*"*50) '''
    rutas = build_ruteo_by_pendientes(fecha,sucursal)
    if rutas:
        ''' print(rutas) '''
        rutas_orm = ruteo_dj_orm(rutas)

        rutas_serialized = RutasSerializer(rutas_orm)
        return Response(rutas_serialized.data)
    return Response({})

@api_view(['GET'])
def sugerencia_ruta_envios(request):
    envs = request.query_params['envios']
    envs = envs.split(",")
    sucursal = request.query_params['sucursal']
    ''' print("*"*50)
    print(sucursal)
    print("*"*50) '''
    rutas = build_ruteo_by_envios(envs, sucursal) 
    if rutas: 
        rutas_orm = ruteo_dj_orm(rutas)
        rutas_serialized = RutasSerializer(rutas_orm)
        return Response(rutas_serialized.data)
    else:
        return Response({})



@api_view(['GET'])
def sugerencia_ruta_optima(request):
    embarque_id = request.query_params['embarque_id']
    ruta = optimizacion_ruta_embarque(embarque_id)
    return JsonResponse(ruta, safe=False)