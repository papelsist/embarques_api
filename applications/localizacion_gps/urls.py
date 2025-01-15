from django.urls import path
from . import views 

urlpatterns = [
     path('api/get_ubicaciones_gps/', views.get_ubicaciones_gps, name='get_ubicacion_gps'),
]