from django.db import models


class EmbarqueManager(models.Manager):

    def pendientes_salida(self):
        embarques = self.filter(or_fecha_hora_salida = None).order_by('-documento')
        return embarques