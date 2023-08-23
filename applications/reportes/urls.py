from django.urls import path
from . import views 

urlpatterns = [
    path('api/embarques/reporte_asignacion', views.imprimirReporteAsignacion, name='imprimirReporteAsignacion'),
    path('api/embarques/reporte_test', views.imprimirReporteTest, name='imprimirReporteTest'),
]