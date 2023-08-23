from django.db import models




class EntregaParcialManager(models.Manager):

    def entregas_transito(self):
        entregas = self.filter(entregas__recorrido__regreso = None)
        return entregas