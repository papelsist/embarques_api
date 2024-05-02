
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
#from applications.embarques.models import Sucursal



class Sucursal(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.BooleanField(default= False)
    clave = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    almacen = models.BooleanField(default= False)
    db_url = models.CharField(max_length=255, blank=True, null=True)
    sx = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=100, blank=True, null=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()
    or_municipio = models.CharField(max_length=255, blank=True, null=True)
    or_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_latitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    direccion_longitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)

    def __str__(self):
        return self.nombre


    class Meta:
        managed = False
        db_table = 'sucursal'

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField(default= 1, blank=True, null=True)
    account_expired =  models.BooleanField(default=False)
    account_locked =   models.BooleanField(default=False)

    # apellido_materno = models.CharField(max_length=255)
    # apellido_paterno = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    nombres = models.CharField(max_length=255)
    puesto = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    numero_de_empleado = models.IntegerField(blank=True, null=True)

    enabled =  models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    password_expired =  models.BooleanField(default=False)
  
    username = models.CharField(unique=True, max_length=255)
    nip = models.CharField(max_length=12, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    sucursal = models.ForeignKey(Sucursal,models.DO_NOTHING,null=True)

    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS= []

    objects = UserManager()

    def get_shortname(self):
        return self.username

    def get_fullname(self):
        return f"{self.nombres} {self.apellidos}"
    
    ''' def save(self, *args, **kwargs):
        self.set_password(self.password)
        super(User, self).save(*args, **kwargs) '''

    class Meta:
        managed = True
        db_table = 'user'