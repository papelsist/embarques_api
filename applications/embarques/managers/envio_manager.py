
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
    
    def find_envio_surtido(self,tipo,documento,fecha,sucursal):
        
        envios = self.get(
            entidad = tipo, documento=documento, fecha_documento = fecha, sucursal = sucursal
        )
        return envios
    
    def pendientes_salida(self,fecha_inicial, fecha_final, sucursal):
        print("Buscando los pendientes de salida")
        
        #envios_list = self.filter(~Q(surtido = None),instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal, pasan= False)
        envios_list = self.filter(instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal, pasan= False)
        envios = [x for x in envios_list if x.enviado == 0.00]
        return envios  
 
    def pendientes_asignacion(self, sucursal):
        
        fecha_final = date.today()
        fecha_inicial = fecha_final - relativedelta(months=2)
        envios_list = self.filter(instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal, pasan= False).order_by('date_created')
        envios = [x for x in envios_list if x.enviado == 0.00]
        return envios  
        
    def envios_parciales(self, fecha_inicial, fecha_final, sucursal):
        envios_list = self.filter(instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal, pasan= False)   
        print(envios_list)
        envios = [x for x in envios_list if x.enviado != 0.00 and x.saldo != 0.00]
        print(envios)
        return envios
    
    def envios_parciales_pendientes(self,sucursal):
        fecha_final = date.today()
        fecha_inicial = fecha_final - relativedelta(months=2)
        envios_list = self.filter(instruccion__fecha_de_entrega__date__range=[fecha_inicial, fecha_final], sucursal=sucursal.nombre, pasan= False)   
        print(envios_list)
        envios = [x for x in envios_list if x.enviado != 0.00 and x.saldo != 0.00]
        print(envios)
        return envios
    

