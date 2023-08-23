from django.urls import path
from . import views 

urlpatterns = [
    #path('api/embarques/facturas_transito', views.facturas_transito, name='facturas_transito'),
    path('api/tableros/pendientes_envio', views.pendientes_envio, name='pendientes_envio'),
    #path('api/embarques/reporte_test', views.imprimirReporteTest, name='imprimirReporteTest'),
]