
from django.db import models
from django.db.models import  Count



class EnvioManager(models.Manager):

    '''  def pendientes_envio(self):
        pendientes = self.filter(
        detalles__entregas__id = None
        ).annotate(
            partidas = Count('id')
        )
        return pendientes '''
    
    def find_envio(self,tipo,documento,fecha):
        envios = self.get(
            entidad = tipo, documento=documento, fecha_documento = fecha
        )
        print(envios.__dict__)

        return envios
