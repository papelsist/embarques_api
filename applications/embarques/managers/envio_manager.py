
from django.db import models
from django.db.models import  Sum,Max,Q,F



class EnvioManager(models.Manager):
    
    def find_envio(self,tipo,documento,fecha,sucursal):
        envios = self.get(
            entidad = tipo, documento=documento, fecha_documento = fecha, sucursal = sucursal
        )
        return envios
    
    def pendientes_salida(self,fecha_inicial, fecha_final, sucursal):
        envios = self.filter(instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal)
        return envios  
 
    

