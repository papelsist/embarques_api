from django.urls import path
from . import views 

urlpatterns = [
    path('api/ruteo/sugerencia_ruta_pendientes', views.sugerencia_ruta_pendientes, name='sugerencia_ruta_pendientes'),
    path('api/ruteo/sugerencia_ruta_envios', views.sugerencia_ruta_envios, name='sugerencia_ruta_envios'),
    path('api/ruteo/sugerencia_ruta_optima', views.sugerencia_ruta_optima, name='sugerencia_ruta_optima'),

]