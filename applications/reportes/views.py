from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

#Importacion de Reportes
from .services import imprimir_reporte_asignacion, imprimir_reporte_test_group



@api_view(['GET'])
def imprimirReporteAsignacion(request):
    #cfdiId = request.GET['cfd']
    reporte = imprimir_reporte_asignacion()
    return HttpResponse(reporte, content_type='application/pdf')
    #return Response({'Test':'Completo'})


@api_view(['GET'])
def imprimirReporteTest(request):
    #cfdiId = request.GET['cfd']
    reporte = imprimir_reporte_test_group()
    return HttpResponse(reporte, content_type='application/pdf')
    #return Response({'Test':'Completo'})