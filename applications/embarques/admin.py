from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Embarque, Envio, EnvioDet,Entrega, EntregaDet, Sucursal


admin.site.register(Embarque)
admin.site.register(Envio)
admin.site.register(EnvioDet)
admin.site.register(Entrega)
admin.site.register(EntregaDet)
admin.site.register(Sucursal)
