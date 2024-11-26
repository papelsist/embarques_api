from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse

#Importacion de Reportes
from .services import imprimir_reporte_asignacion, imprimir_reporte_test_group,imprimir_reporte_ruta, imprimir_reporte_asignacion_embarque, imprimir_reporte_entrega



@api_view(['GET'])
def imprimirReporteAsignacion(request):
    embarque_id= request.query_params['embarqueId']
    reporte = imprimir_reporte_asignacion(embarque_id)
    return HttpResponse(reporte, content_type='application/pdf')
  


@api_view(['GET'])
def imprimirReporteTest(request):
    print(request)
    reporte = imprimir_reporte_test_group(66)
    return HttpResponse(reporte, content_type='application/pdf')

@api_view(['POST'])
def imprimirSugerenciaRuta(request):
    reporte = imprimir_reporte_ruta(request.data)
    return HttpResponse(reporte, content_type='application/pdf')


@api_view(['GET'])
def imprimirReporteAsignacionEmbarque(request):
    embarque_id= request.query_params['embarqueId']
    reporte = imprimir_reporte_asignacion_embarque(embarque_id)
    return HttpResponse(reporte, content_type='application/pdf')
    #return Response({'message': 'Hello, world!'})

@api_view(['GET'])
@permission_classes([AllowAny])
def imprimirReporteEntregaDoctos(request):
    operador_id= request.query_params['operador_id']
    sucursal_id = request.query_params['sucursal_id']
    fecha = request.query_params['fecha']
    print(request.query_params)
    reporte = imprimir_reporte_entrega(operador_id, sucursal_id, fecha)
    return HttpResponse(reporte, content_type='application/pdf')
    