from django.urls import path
from . import views 

urlpatterns = [
    path('api/embarques/reporte_asignacion', views.imprimirReporteAsignacion, name='imprimirReporteAsignacion'),
    path('api/embarques/reporte_test', views.imprimirReporteTest, name='imprimirReporteTest'),
    path('api/embarques/sugerencia_ruta', views.imprimirSugerenciaRuta, name='imprimirSugerenciaRuta'),
    path('api/embarques/reporte_asignacion_embarque', views.imprimirReporteAsignacionEmbarque, name='imprimirReporteAsignacionEmbarque'),
    path('api/embarques/reporte_entrega_doctos', views.imprimirReporteEntregaDoctos, name='imprimirReporteEntregaDoctos'),
    path('api/embarques/reporte_pendientes_pago', views.imprimirReportePendientesPago, name='imprimirReportePendientesPago'),
    path('api/embarques/reporte_pendientes_doctos', views.imprimirReportePendientesDoctos, name='imprimirReportePendientesDoctos'),
    path('api/embarques/reporte_envios_callcenter', views.imprimirReporteEnviosCallcenter, name='imprimirReporteCallcenter'),

]