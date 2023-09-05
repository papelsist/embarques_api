from django.db import models


class FolioManager(models.Manager):

    def get_folio(self, serie):
        folio = self.get( serie = serie)
        return folio.folio

    def get_next_folio(self, serie):
        folio = self.get( serie = serie)
        return folio.folio + 1
    
    def  set_folio(self,serie):
        folio = self.get( serie = serie)
        folio.folio +=1
        folio.save()
        return folio.folio
    
    def set_next_folio(self, serie, new_folio):
        folio = self.get( serie = serie)
        folio.folio = new_folio
        folio.save()
        return folio.folio