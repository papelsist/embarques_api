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
    path('api/embarques/asignar_envios_pendientes', views.asignar_envios_pendientes, name='asignar_evios_pendientes'),
    path('api/embarques/asignar_envios_parciales', views.asignar_envios_parciales, name='asignar_envios_parciales'),
    path('api/embarques/transito_operador', views.TransitoOperador.as_view(), name='transito_operador'),
    path('api/embarques/regresos_operador', views.RegresosOperador.as_view(), name='regresos_operador'),
    path('api/embarques/ruta_embarque/<pk>', views.RutaEmbarque.as_view(), name='ruta_embarque'),
    path('api/embarques/ruta_entrega/<pk>', views.EntregaRuta.as_view(), name='ruta_entrega'),
    path('api/embarques/test', views.test_view, name='test'),
    path('api/embarques/crear_incidencia', views.crear_incidencia_entrega, name='crear_incidencia'),
    path('api/embarques/entregas_incidencias', views.IncidenciasEntrega.as_view(), name='entregas_incidencias'),
    path('api/embarques/incidencia/<pk>', views.Incidencia.as_view(), name='incidencia'),
    path('api/embarques/validar_cercania', views.validar_cercania, name='validar_cercania'),
    path('api/embarques/crear_embarque_operador', views.crear_embarque_operador, name='crear_embarque_operador'),
    path('api/embarques/crear_seguimiento', views.crear_seguimiento, name='crear_seguimiento'),
    path('api/embarques/envios_parciales/', views.EnviosParciales.as_view(), name='embarques_parciales'),
    path('api/embarques/envios_parciales/<pk>/', views.GetEnvio.as_view(), name='embarques_parciales'),
    path('api/embarques/actualizar_fecha_entrega', views.actualizar_fecha_entrega, name='actualizar_fecha_entrega'),
    path('api/embarques/actualizar_pasan_total', views.actualizar_pasan_total, name='actualizar_pasan_total'),
    path('api/embarques/asignar_pasan/', views.asignar_pasan, name='asignar_pasan'),
    path('api/embarques/embarques_pasan/', views.EmbarquesPasan.as_view(), name='embarques_pasan'),
    path('api/embarques/search_entrega/', views.search_entrega_mtto, name='search_entrega'),
    path('api/embarques/actualizar_bitacora_entrega/', views.actualizar_bitacora_entrega, name='actualizar_bitacora_entregas'),
]