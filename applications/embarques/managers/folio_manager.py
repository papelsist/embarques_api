from django.db import models


class FolioManager(models.Manager):

    def get_folio(self, serie,sucursal):
        folio = self.get( serie = serie, sucursal_id = sucursal)
        return folio.folio

    def get_next_folio(self, serie, sucursal):
        folio = self.get( serie = serie, sucursal_id = sucursal)
        return folio.folio + 1
    
    def  set_folio(self,serie, sucursal):
        folio = self.get( serie = serie, sucursal_id = sucursal)
        folio.folio +=1
        folio.save()
        return folio.folio
    
    def set_next_folio(self, serie, new_folio,sucursal):
        folio = self.get( serie = serie, sucursal_id = sucursal)
        folio.folio = new_folio
        folio.save()
        return folio.folio