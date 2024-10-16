from django.urls import path
from . import views 

urlpatterns = [
    path('api/tableros/pendientes_asignacion', views.EnviosPendientesAsignacion.as_view(), name='pendientesAsignacion'),
    path('api/tableros/embarques_pendientes_salida', views.EmbarquesPendientesSalida.as_view(), name='embarquesPendientesSalida'),
    path('api/tableros/embarques_transito', views.EmbarquesTransito.as_view(), name='embarquesTransito'),
    path('api/tableros/envios_transito', views.EnviosTransito.as_view(), name='enviosTransito'),
    path('api/tableros/envios_parciales', views.EnviosParciales.as_view(), name='enviosParciales'),
]