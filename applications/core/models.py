from django.db import models
import uuid

# Create your models here.

class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.BigIntegerField()
    certificado_digital = models.BinaryField(blank=True, null=True)
    certificado_digital_pfx = models.BinaryField(blank=True, null=True)
    clave = models.CharField(unique=True, max_length=15)
    llave_privada = models.BinaryField(blank=True, null=True)
    nombre = models.CharField(unique=True, max_length=255)
    numero_de_certificado = models.CharField(max_length=20, blank=True, null=True)
    password_pac = models.CharField(max_length=255, blank=True, null=True)
    password_pfx = models.CharField(max_length=255, blank=True, null=True)
    regimen = models.CharField(max_length=300)
    rfc = models.CharField(max_length=13)
    timbrado_de_prueba = models.BooleanField(default=True) 
    usuario_pac = models.CharField(max_length=255, blank=True, null=True)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_latitud = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    direccion_longitud = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    regimen_clave_sat = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'empresa'

class Sucursal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.BigIntegerField(default=0)
    activa = models.BooleanField(default=True)
    clave = models.CharField(unique=True, max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    nombre = models.CharField(unique=True, max_length=255)
    sw2 = models.BigIntegerField(blank=True, null=True)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_latitud = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    direccion_longitud = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    almacen = models.BooleanField(default=True)
    db_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sucursal'


class CodigosPostalesMX(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estado = models.CharField(max_length=255, blank=True, null=True)
    asentamiento = models.CharField(max_length=255, blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True, null=True)
    colonia = models.CharField(max_length=255, blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=255, blank=True, null=True)
    municipio_sat = models.CharField(max_length=255, blank=True, null=True)
    localidad_sat = models.CharField(max_length=255, blank=True, null=True)
    codigo_sat = models.CharField(max_length=255, blank=True, null=True)
    estado_sat = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)
    #date_created = models.DateTimeField(auto_now_add=True, null=True)
    #last_updated = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        managed = True
        db_table = 'codigos_postales_mx'
