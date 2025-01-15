from django.db import models

# Create your models here.

class Tokens(models.Model):
    servicio = models.CharField(max_length=200)
    token = models.CharField(max_length=200, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'tokens'
