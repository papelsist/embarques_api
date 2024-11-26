from django.db import models
from django.db.models import Q, F, Count,Max, Sum, Min


class EmbarqueManager(models.Manager):

    def pendientes_salida(self, sucursal):
        embarques = self.filter(or_fecha_hora_salida = None, sucursal= sucursal).order_by('documento')
        return embarques
    
    def transito(self, sucursal):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),regreso = None, sucursal = sucursal ).order_by('documento')
        return embarques
    
    def regresos(self,fecha_inicial, fecha_final,sucursal):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None), ~Q(operador__nombre = 'CLIENTE PASAN'),~Q(regreso = None), regreso__date__range=[fecha_inicial, fecha_final], sucursal = sucursal).order_by('documento')

        return embarques
    
    def embarques_pasan(self,fecha_inicial, fecha_final,sucursal):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),~Q(regreso = None), regreso__date__range=[fecha_inicial, fecha_final], sucursal = sucursal, operador__nombre = 'CLIENTE PASAN').order_by('documento')
        return embarques
    
    def transito_operador(self, operador):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),regreso = None, operador = operador ).order_by('documento')
        return embarques
    
    def regresos_operador(self,fecha_inicial, fecha_final,operador):
        embarques = self.filter( ~Q(or_fecha_hora_salida = None),~Q(regreso = None), fecha__range=[fecha_inicial, fecha_final], operador = operador).order_by('documento')
        return embarques
    
    def embarque_by_documento_fecha(self,documento,fecha, sucursal):
        embarque = self.filter(documento = documento, fecha = fecha, sucursal = sucursal).first()
        return embarque
    
    def embarques_operador_kilos(self,fecha_inicial, fecha_final):
        embarques = (self.filter( fecha__range=[fecha_inicial, fecha_final])
                     .values( 'operador__id','operador__nombre')
                     .annotate(  
                            fecha_inicial = Min('fecha'),
                            fecha_final = Max('fecha'),
                            valor = Sum('partidas__detalles__kilos'),      
                        )
                     )
        print(embarques.query)
        return embarques
        
    
 