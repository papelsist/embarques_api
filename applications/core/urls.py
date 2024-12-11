from django.urls import path
from . import views 

urlpatterns = [
    path('api/get_address_from_zipcode/', views.get_address_from_zipcode, name='get_address_from_zipcode' ), 
]