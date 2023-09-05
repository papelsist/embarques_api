from django.db import models




class EntregaManager(models.Manager):

    def entregas_transito(self):
        entregas = self.filter(entregas__recorrido__regreso = None)
        return entregas