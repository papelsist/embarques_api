from django.db import models




class EntregaManager(models.Manager):
    def entregas_transito(self):
        entregas = self.filter(entregas__recorrido__regreso = None)
        return entregas
    

class EntregaIncidenciaManager(models.Manager):
    def incidencias_periodo(self, fecha_inicio, fecha_fin):
        incidencias = self.filter(fecha__range=[fecha_inicio, fecha_fin])
        return incidencias

    

