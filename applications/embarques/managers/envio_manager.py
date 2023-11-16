
from django.db import models
from django.db.models import  Sum,Max,Q,F
from datetime import date
from dateutil.relativedelta import relativedelta


class EnvioManager(models.Manager):
    
    def find_envio(self,tipo,documento,fecha,sucursal):
        envios = self.get(
            entidad = tipo, documento=documento, fecha_documento = fecha, sucursal = sucursal
        )
        return envios
    
    def pendientes_salida(self,fecha_inicial, fecha_final, sucursal):
        print("Buscando los pendientes de salida")
        envios = self.filter(instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal)
        return envios  
 
    def pendientes_asignacion(self, sucursal):
        envios = self.filter
        fecha_final = date.today()
        fecha_inicial = fecha_final - relativedelta(months=2)
        print(fecha_inicial)
        print(fecha_final)
        envios = self.filter(instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal)
        return envios  
        
    

