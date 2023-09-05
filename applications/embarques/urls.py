from django.urls import path
from . import views 

urlpatterns = [
    path('api/embarques/facturas_transito', views.facturas_transito, name='facturas_transito'),
     #path('api/embarques/reporte_test', views.imprimirReporteTest, name='imprimirReporteTest'),
    path('api/tableros/pendientes_envio', views.pendientes_envio, name='pendientes_envio'),
    path('api/tableros/transito_envio', views.transito_envio, name='transito_envio'),
    path('api/embarques/pendientes_salida', views.PendientesSalida.as_view(), name='pendientes_salida'),
    path('api/embarques/search_operador', views.SearchOperador.as_view(), name='search_operador'),
    path('api/embarques/search_envio', views.search_envio, name='search_envio'),
    path('api/embarques/crear_embarque', views.crear_embarque, name='crear_embarque'),
    path('api/embarques/crear_asignacion/<pk>', views.CrearAsignacion.as_view(), name='crear_asignacion'),
    path('api/embarques/actualizar_embarque',views.actualizar_embarque , name='actualizar_embarque'),
    
]