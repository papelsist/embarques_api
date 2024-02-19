from django.db import models
from django.db.models import Q


class EmbarqueManager(models.Manager):

    def pendientes_salida(self, sucursal):
        embarques = self.filter(or_fecha_hora_salida = None, sucursal= sucursal).order_by('-documento')
        return embarques
    
    def transito(self, sucursal):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),regreso = None, sucursal = sucursal ).order_by('documento')
        return embarques
    
    def regresos(self,fecha_inicial, fecha_final,sucursal):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),~Q(regreso = None), fecha__range=[fecha_inicial, fecha_final], sucursal = sucursal).order_by('documento')
        return embarques
    
    def transito_operador(self, operador):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),regreso = None, operador = operador ).order_by('documento')
        return embarques
    
    def regresos_operador(self,fecha_inicial, fecha_final,operador):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),~Q(regreso = None), fecha__range=[fecha_inicial, fecha_final], operador = operador).order_by('documento')
        return embarques
        
    
 