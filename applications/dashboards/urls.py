from django.urls import path
from . import views 

urlpatterns =  [
    path('api/dashboards/embarques_operador', views.embarques_operador),
]