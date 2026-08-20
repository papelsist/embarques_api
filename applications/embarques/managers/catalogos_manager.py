from django.db import models


class OperadorManager(models.Manager):
    
    def find_operador(self, term):
        if not term:
            return self.none()
        return self.filter(nombre__icontains=term).order_by('nombre').distinct()