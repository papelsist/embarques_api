from django.urls import path
from . import views 

urlpatterns = [
    path('api/tableros/pendientes_envio', views.pendientes_envio, name='pendientes_envio'),
    path('api/tableros/transito_envio', views.transito_envio, name='transito_envio'),
    path('api/embarques/pendientes_salida', views.PendientesSalida.as_view(), name='pendientes_salida'),
    path('api/embarques/search_operador', views.SearchOperador.as_view(), name='search_operador'),
    path('api/embarques/search_envio', views.search_envio, name='search_envio'),
    path('api/embarques/crear_embarque', views.crear_embarque, name='crear_embarque'),
    path('api/embarques/crear_asignacion/<pk>', views.CrearAsignacion.as_view(), name='crear_asignacion'),
    path('api/embarques/actualizar_embarque',views.actualizar_embarque , name='actualizar_embarque'),
    path('api/embarques/eliminar_entrega_det',views.eliminar_entrega_det , name='eliminar_entrega_det'),
    path('api/embarques/registrar_salida',views.registrar_salida , name='registrar_salida'),
    path('api/embarques/borrar_embarque',views.eliminar_embarque , name='borrar_embarque'),
    path('api/embarques/transito', views.Transito.as_view(), name='transito'),
    path('api/embarques/actualizar_entregas/<pk>', views.ActualizarEntregas.as_view(), name='actualizar_entregas'),
    path('api/embarques/actualizar_bitacora', views.actualizar_bitacora, name='actualizar_bitacora'),
    path('api/embarques/eliminar_entrega', views.eliminar_entrega, name='eliminar_entrega'),
    path('api/embarques/registrar_regreso', views.registrar_regreso, name='registrar_regreso'),
    path('api/embarques/regresos', views.Regresos.as_view(), name='regresos'),
    path('api/embarques/envios_pendientes', views.EnviosPendientes.as_view(), name='envios_pendientes'),
    path('api/embarques/embarque_ruteo', views.embarque_por_ruteo, name='embarque_por_ruteo'),
    path('api/embarques/asignar_evios_pendientes', views.asignar_evios_pendientes, name='asignar_evios_pendientes'),
]