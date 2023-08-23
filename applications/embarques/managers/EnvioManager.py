
from django.db import models



class EnvioManager(models.Manager):

    def pendientes_envio(self):
        pendientes = self.filter(
        detalles__entregas__id = None
        )
       
        return pendientes

