from django.db import models


class OperadorManager(models.Manager):
    
    def find_operador(self, term):
        founds = self.filter(nombre__icontains = term)
        return founds