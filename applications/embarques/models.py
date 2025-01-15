from django.db import models
from django.db.models import  Q
from .managers import EnvioManager,EntregaManager, OperadorManager, FolioManager,EmbarqueManager, EntregaIncidenciaManager
from applications.authentication.models import User
from applications.core.models import Sucursal,Empresa
import uuid



""" Modelos de Catalogos"""

class TransporteForaneo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    direccion_latitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    direccion_longitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    telefono3 = models.CharField(max_length=255, blank=True, null=True)
    telefono2 = models.CharField(max_length=255, blank=True, null=True)
    telefono1 = models.CharField(max_length=255, blank=True, null=True)
    sucursal = models.CharField(max_length=255, blank=True, null=True)
    sx = models.CharField(max_length=255, unique=True, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'transporte_foraneo'


class FacturistaEmbarques(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    rfc = models.CharField(unique=True, max_length=13)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    descuent_en_prestamo = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    orden = models.BigIntegerField()
    sx = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=100, blank=True, null=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()
    clave = models.CharField(max_length=6)

    class Meta:
        managed = True
        db_table = 'facturista_embarques'

class Propietario(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.BooleanField(default= True) 
    facturista = models.ForeignKey(FacturistaEmbarques, models.DO_NOTHING)
    rfc = models.CharField(unique=True, max_length=13)
    nombre = models.CharField(max_length=255)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=100, blank=True, null=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'propietario'

class CpFacturista(models.Model):
    id = models.BigAutoField(primary_key=True)
    facturista = models.OneToOneField(FacturistaEmbarques, models.DO_NOTHING)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    regimen = models.CharField(max_length=300)
    llave_privada = models.TextField(blank=True, null=True)
    numero_de_certificado = models.CharField(max_length=20, blank=True, null=True)
    certificado_digital = models.TextField(blank=True, null=True)
    certificado_digital_pfx = models.TextField(blank=True, null=True)
    password_pac = models.CharField(max_length=255, blank=True, null=True)
    password_pfx = models.CharField(max_length=255, blank=True, null=True)
    timbrado_de_prueba = models.TextField()  # This field type is a guess.
    usuario_pac = models.CharField(max_length=255, blank=True, null=True)
    version_de_cfdi = models.CharField(max_length=3)
    regimen_clave_sat = models.CharField(max_length=20, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'cp_facturista'





class Folio(models.Model):
    id = models.BigAutoField(primary_key=True)
    entidad = models.CharField(max_length=255, blank=True, null=True)
    folio = models.BigIntegerField()
    serie = models.CharField(max_length=255, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal,models.DO_NOTHING,null=True)
    sucursal_nombre  = models.CharField(max_length=50, blank=True, null=True)

    objects = FolioManager()

    class Meta:
        managed = False
        db_table = 'folio'

""" Modelos de  Embarques"""

class Embarque(models.Model):
    id = models.BigAutoField(primary_key=True)
    documento = models.IntegerField(blank=True, null=True)
    operador = models.ForeignKey('Operador', models.DO_NOTHING)
    sucursal = models.ForeignKey(Sucursal, models.DO_NOTHING)
    facturista = models.ForeignKey('FacturistaEmbarques', models.DO_NOTHING)
    fecha = models.DateField()
    or_fecha_hora_salida = models.DateTimeField(blank=True, null=True)
    regreso = models.DateTimeField(blank=True, null=True)
    cerrado = models.DateTimeField(blank=True, null=True)
    valor = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    kilos = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    importe_comision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    facturado = models.DateTimeField(blank=True, null=True)
    cancelado = models.DateTimeField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    empleado = models.CharField(max_length=255, blank=True, null=True)
    sx = models.CharField(unique=True, max_length=255, blank=True, null=True)
    me_num_total_mercancias = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField(blank=True, null= True)
    cp = models.BooleanField(default= False)

    objects = EmbarqueManager()

    class Meta:
        managed = True
        db_table = 'embarques'

class Entrega(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.ForeignKey('Envio', models.DO_NOTHING, related_name='entregas')
    embarque = models.ForeignKey(Embarque, models.DO_NOTHING,related_name='partidas')
    sucursal = models.CharField(max_length=255)
    destinatario = models.CharField(max_length=255, blank=True, null=True)
    operador = models.CharField(max_length=255, blank=True, null=True)
    origen = models.CharField(max_length=255, blank=True, null=True)
    entidad = models.CharField(max_length=255)
    realizo = models.CharField(max_length=255, blank=True, null=True)
    fecha_documento = models.DateTimeField()
    documento = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=255)
    forma_pago = models.CharField(max_length=255, blank=True, null=True)
    paquetes = models.IntegerField(blank=True, null=True)
    kilos = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    total_documento = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    valor = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    arribo = models.DateTimeField(blank=True, null=True)
    arribo_latitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True,null=True)
    arribo_longitud = models.DecimalField(max_digits=19, decimal_places=7, blank= True, null=True)
    recepcion = models.DateTimeField(blank=True, null=True)
    recepcion_latitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    recepcion_longitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    regreso = models.DateTimeField(blank=True, null=True)
    recibio = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    reporto_nombre = models.CharField(max_length=255, blank=True, null=True)
    reporto_puesto = models.CharField(max_length=255, blank=True, null=True)
    recepcion_pago = models.DateTimeField(max_length=255, blank=True, null=True)
    recepcion_documentos = models.DateTimeField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)

    objects = EntregaManager()

    class Meta:
        managed = True
        db_table = 'entrega'

class ImgEntrega(models.Model):

    id = models.BigAutoField(primary_key=True)
    entrega = models.ForeignKey('Entrega', models.CASCADE,related_name='imagenes')
    url_image = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'img_entrega'




class EntregaDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    entrega = models.ForeignKey('Entrega', models.CASCADE,related_name='detalles')
    envio_det = models.ForeignKey('EnvioDet', models.DO_NOTHING, related_name='entregas')
    sx_instruccion_de_envio = models.CharField(max_length=255, blank=True, null=True)
    almacen = models.CharField(max_length=255, blank=True, null=True)
    instruccion_de_entrega_parcial = models.CharField(max_length=255, blank=True, null=True)
    clave = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=19, decimal_places=2)
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    kilos = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    @property
    def saldo(self): 
        return self.envio_det.saldo
    
    @property
    def enviado(self):
        return self.envio_det.enviado
    
    @property
    def cantidad_envio(self):
        return self.envio_det.me_cantidad

    class Meta:
        managed = True
        db_table = 'entrega_det'


    
class EntregaComision(models.Model):
    id = models.BigAutoField(primary_key=True)
    entrega = models.ForeignKey('Entrega', models.DO_NOTHING)
    valor = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    valor_caja = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    precio_tonelada = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    maniobra = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    importe_comision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comision_por_tonelada = models.BooleanField(default= False) 
    comentario_comision = models.CharField(max_length=255, blank=True, null=True)
    fecha_comision = models.DateTimeField(blank=True, null=True)
    manual = models.BooleanField(default= False)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'entrega_comision'


class EntregaIncidencia(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.ForeignKey('Envio', models.DO_NOTHING, related_name='incidencias', null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    folio = models.IntegerField(blank=True, null=True)
    #### Datos Embarque
    embarque = models.CharField(max_length=255, null=True)
    #### Datos Entrega
    sucursal = models.CharField(max_length=255, null=True)
    destinatario = models.CharField(max_length=255, blank=True, null=True)
    operador = models.CharField(max_length=255, blank=True, null=True)
    origen = models.CharField(max_length=255, blank=True, null=True)
    entidad = models.CharField(max_length=255, null=True)
    realizo = models.CharField(max_length=255, blank=True, null=True)
    fecha_documento = models.DateTimeField(null=True)
    documento = models.CharField(max_length=255, null=True)
    tipo_documento = models.CharField(max_length=255, null=True)
    #### Datos EntregaDet
    clave = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    valor = models.DecimalField(max_digits=19, decimal_places=2,default=0)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    devuelto = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    entregado = models.BooleanField(default= False) 
    incompleto = models.BooleanField(default= False) 
    maltratado = models.BooleanField(default= False) 
    impreso = models.BooleanField(default= False) 
    cortado = models.BooleanField(default= False)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    img1 = models.CharField(max_length=255, blank=True, null=True)
    img2 = models.CharField(max_length=255, blank=True, null=True)
    img3 = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects= EntregaIncidenciaManager()

    class Meta:
        managed = True
        db_table = 'entrega_incidencia'

class EntregaIncidenciaSeguimiento(models.Model):

    id = models.BigAutoField(primary_key=True)
    incidencia = models.ForeignKey(EntregaIncidencia, models.DO_NOTHING, related_name='seguimientos')
    fecha = models.DateField(auto_now_add=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'entrega_incidencia_seguimiento'



''' class EntregaRecorrido(models.Model):
    id = models.BigAutoField(primary_key=True)
    entrega = models.ForeignKey(Entrega, models.DO_NOTHING, related_name="recorrido")
    salida = models.DateTimeField(blank=True, null=True)
    arribo = models.DateTimeField(blank=True, null=True)
    arribo_latitud = models.DecimalField(max_digits=19, decimal_places=2)
    arribo_longitud = models.DecimalField(max_digits=19, decimal_places=2)
    recepcion = models.DateTimeField(blank=True, null=True)
    recepcion_latitud = models.DecimalField(max_digits=19, decimal_places=2)
    recepcion_longitud = models.DecimalField(max_digits=19, decimal_places=2)
    regreso = models.DateTimeField(blank=True, null=True)
    recibio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'entrega_recorrido' '''


class Envio(models.Model):
    id = models.BigAutoField(primary_key=True)
    sucursal = models.CharField(max_length=255)
    origen = models.CharField(max_length=255)
    entidad = models.CharField(max_length=255)
    # Este dato debe ser de tipo Date no DateT
    fecha_documento = models.DateTimeField()
    documento = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=255)
    forma_pago = models.CharField(max_length=255, blank=True, null=True)
    pagado = models.BooleanField(default= False)
    kilos = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    total_documento = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    callcenter = models.CharField(max_length=255, blank=True, null=True)
    sx = models.CharField(unique=True, max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()
    realizo = models.CharField(max_length=255, blank=True, null=True)
    destinatario = models.CharField(max_length=255, blank=True, null=True)
    pasan = models.BooleanField(default= False) 
    usuario_pasan = models.CharField(max_length=255, blank=True, null=True)
    #
    de_rfc_destinatario = models.CharField(max_length=13, blank=True, null=True)
    de_destino = models.CharField(max_length=100, blank=True, null=True)
    maniobra = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True,default=0.00)
    email_envio = models.CharField(max_length=255, blank=True, null=True)
    surtido = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)



    
    @property
    def saldo(self):
        envios = EnvioDet.objects.filter(~Q(clave = 'CORTE'),envio = self)
        saldo = sum(env.saldo for env in envios)
        return saldo 
    
    @property
    def por_enviar(self):
        envios = EnvioDet.objects.filter(~Q(clave = 'CORTE'),envio = self)
        por_enviar = sum(env.me_cantidad for env in envios)
        return por_enviar
    @property
    def enviado(self):
        enviado = self.por_enviar - self.saldo
        return enviado
  

    objects = EnvioManager()

    class Meta:
        managed = True
        db_table = 'envio'


class EnvioDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.ForeignKey(Envio, models.DO_NOTHING,related_name="detalles")
    origen_det_sx = models.CharField(max_length=255, blank=True, null=True)
    producto_sx = models.CharField(max_length=255)
    clave = models.CharField(max_length=255)
    me_descripcion = models.CharField(max_length=255)
    me_kilos = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    moneda = models.CharField(max_length=3)
    me_cantidad = models.DecimalField(max_digits=19, decimal_places=2)
    instruccion_entrega = models.CharField(max_length=255, blank=True, null=True)
    sx = models.CharField(unique=True, max_length=255, blank=True, null=True)
    me_unidad = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()
    cortes = models.CharField(max_length=300, blank=True, null=True)
    kxmil= models.DecimalField(max_digits=19, decimal_places=3, blank=True, null=True, default=0.000)
    me_bienes_transp = models.CharField(max_length=255, blank=True, null=True, default='sin variable') 
    me_clave_unidad = models.CharField(max_length=10, blank=True, null=True, default='no info')
    me_material_peligroso = models.CharField(max_length=2, blank=True, null=True, default='No')
    surtido = models.DateTimeField(blank=True, null=True)
    surtidor = models.CharField(max_length=255, blank=True, null=True)


    @property
    def saldo(self):
        entrega = EntregaDet.objects.filter(envio_det = self)
        enviado = sum(ent.cantidad for ent in entrega)
        saldo = self.me_cantidad - enviado
        return saldo 
    
    @property
    def enviado(self):
        entrega = EntregaDet.objects.filter(envio_det = self)
        enviado = sum(ent.cantidad for ent in entrega)
       
        return enviado



    class Meta:
        managed = True
        db_table = 'envio_det'

class EnvioAnotaciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.ForeignKey(Envio, models.DO_NOTHING, related_name='anotaciones')
    fecha = models.DateField()
    anotacion = models.CharField(max_length=600)
    revisada = models.BooleanField(default= False)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    last_updated = models.DateTimeField(auto_now=True, null= True)

    class Meta:
        managed = True
        db_table = 'envio_anotaciones'
    
class InstruccionDeEnvio(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.OneToOneField(Envio, models.DO_NOTHING, related_name='instruccion' )
    tipo = models.CharField(max_length=255, blank=True, null=True)
    contacto = models.CharField(max_length=255, blank=True, null=True)
    horario = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    direccion_latitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    direccion_longitud = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    fecha_de_entrega = models.DateTimeField(blank=True, null=True)
    sx_transporte = models.ForeignKey(TransporteForaneo,on_delete=models.DO_NOTHING,db_column='sx_transporte', to_field='sx', related_name='transporte_foraneo', null= True, blank=True)
    sx = models.CharField(unique=True, max_length=255, blank=True, null=True)
    distancia = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    sector = models.IntegerField(blank=True, null=True, default= 0)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    #
    origen_sx = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField(default=0)
    email_envio = models.CharField(max_length=255, blank=True, null=True)
    tipo_envio = models.CharField(max_length=255, blank=True, null=True)
    clasificcion_vale = models.CharField(max_length=255, blank=True, null=True)
    distancia = models.DecimalField(max_digits=19, decimal_places=7, blank=True, null=True)
    sector = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'instruccion_de_envio'

""" Modelos de Surtido parciales"""


class DireccionEntrega (models.Model):
    id = models.BigAutoField(primary_key=True)
    clave = models.CharField(max_length=255)
    principal = models.BooleanField(default= False)
    destinatario = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    numero_exterior = models.CharField(max_length=255)
    numero_interior = models.CharField(max_length=255, blank=True, null=True)
    colonia = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    latitud = models.DecimalField(max_digits=19, decimal_places=7)
    longitud = models.DecimalField(max_digits=19, decimal_places=7)
    version = models.BigIntegerField( default=0)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    last_updated = models.DateTimeField(auto_now=True, null= True)

    class Meta:
        managed = True
        db_table = 'direccion_entrega'


class PreEntrega(models.Model): 
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    envio = models.ForeignKey(Envio, models.DO_NOTHING, related_name='preentregas')
    sucursal = models.CharField(max_length=255)
    destinatario = models.CharField(max_length=255, blank=True, null=True)
    documento = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=5, blank=True, null=True)
    fecha_documento = models.DateTimeField()
    surtido = models.DateTimeField(blank=True, null=True)
    enviado = models.DateTimeField(blank=True, null=True)
    direccion_entrega = models.ForeignKey(DireccionEntrega, models.DO_NOTHING, blank=True, null=True )
    fecha_entrega = models.DateField(blank=True, null=True)
    entrega = models.ForeignKey(Entrega, models.DO_NOTHING, blank=True, null=True)
    folio =  models.CharField(max_length=255, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    last_updated = models.DateTimeField(auto_now=True, null= True)

    

    class Meta:
        managed = True
        db_table = 'pre_entrega'

class PreEntregaDet(models.Model):
    id= models.BigAutoField(primary_key=True)
    preentrega = models.ForeignKey(PreEntrega, models.DO_NOTHING, related_name='detalles')
    envio_det = models.ForeignKey(EnvioDet, models.DO_NOTHING, related_name='preentregas')
    cantidad = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    cortes = models.CharField(max_length=255, blank=True, null=True)
    clave = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    surtido = models.DateTimeField(blank=True, null=True)
    surtidor = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    last_updated = models.DateTimeField(auto_now=True, null= True)


    class Meta:
        managed = True
        db_table = 'pre_entrega_det'

""" Modelos de carta porte"""



class CpCfdi(models.Model):
    id = models.BigAutoField(primary_key=True)
    embarque = models.ForeignKey('Embarque', models.DO_NOTHING)
    fecha = models.DateTimeField()
    tipo_de_comprobante = models.CharField(max_length=1)
    origen = models.CharField(max_length=12)
    serie = models.CharField(max_length=30, blank=True, null=True)
    folio = models.CharField(max_length=30, blank=True, null=True)
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    subtotal = models.DecimalField(db_column='subTotal', max_digits=19, decimal_places=2)  # Field name made lowercase.
    impuesto = models.DecimalField(max_digits=19, decimal_places=2)
    retencion_iva = models.DecimalField(max_digits=19, decimal_places=2)
    retencion_isr = models.DecimalField(max_digits=19, decimal_places=2)
    total = models.DecimalField(max_digits=19, decimal_places=2)
    emisor_rfc = models.CharField(max_length=13)
    emisor = models.CharField(max_length=255)
    file_name = models.CharField(max_length=150)
    receptor_rfc = models.CharField(max_length=13)
    receptor = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    status = models.CharField(max_length=255, blank=True, null=True)
    cancelado = models.IntegerField(blank=True, null=True)
    cancel_status = models.CharField(max_length=255, blank=True, null=True)
    comentario_cancel = models.CharField(max_length=255, blank=True, null=True)
    status_code = models.CharField(max_length=200, blank=True, null=True)
    is_cancelable = models.CharField(max_length=255, blank=True, null=True)
    enviado = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    regimen = models.CharField(max_length=255, blank=True, null=True)
    domicilio_fiscal = models.CharField(max_length=255, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    version_cfdi = models.CharField(max_length=3)
    xml = models.TextField()
    uuid_relacionado = models.CharField(max_length=255, blank=True, null=True)
    tipo_de_relacion = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'cp_cfdi'


class CpEmbarques(models.Model):
    id = models.BigAutoField(primary_key=True)
    embarque = models.OneToOneField('Embarque', models.DO_NOTHING)
    cp_version = models.CharField(max_length=20, blank=True, null=True)
    cp_transp_internac = models.CharField(max_length=20, blank=True, null=True)
    cp_total_distancia_recorrida = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    or_origen = models.CharField(max_length=20, blank=True, null=True)
    or_rfc_remitente = models.CharField(max_length=255)
    or_cliente_remitente = models.CharField(max_length=255, blank=True, null=True)
    me_unidad_peso = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()
    cliente = models.ForeignKey(Empresa, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'cp_embarques'


class CpEnvio(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.OneToOneField('Envio', models.DO_NOTHING)
    de_destino = models.CharField(max_length=20, blank=True, null=True)
    de_rfc_destinatario = models.CharField(max_length=255, blank=True, null=True)
    de_destinatario = models.CharField(max_length=255)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'cp_envio'


class CpEnvioDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio_det_id = models.BigIntegerField(unique=True)
    me_bienes_transp = models.CharField(max_length=255, blank=True, null=True)
    me_clave_unidad = models.CharField(max_length=255, blank=True, null=True)
    me_material_peligroso = models.CharField(max_length=2, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'cp_envio_det'





class CpInstruccionDeEnvio(models.Model):
    id = models.BigAutoField(primary_key=True)
    instruccion = models.OneToOneField('InstruccionDeEnvio', models.DO_NOTHING)
    ub_distancia_recorrida = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    de_fecha_hora_progllegada = models.DateTimeField(blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'cp_instruccion_de_envio'


class GeolocalizacionTransportes(models.Model):
    id = models.BigAutoField(primary_key=True)
    transporte = models.ForeignKey('TransporteForaneo', models.DO_NOTHING,related_name='ubicaciones')
    latitud = models.DecimalField(max_digits=19, decimal_places=7)
    longitud = models.DecimalField(max_digits=19, decimal_places=7)
    sucursal = models.CharField(max_length=255, blank=True, null=True)
    distancia = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    version = models.BigIntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'geolocalizacion_transportes'

class TransporteEmbarques(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.BooleanField(default= False)
    marca = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    iv_anio_modelo = models.CharField(max_length=255, blank=True, null=True)
    iv_placa_vm = models.CharField(unique=True, max_length=255)
    af_nombre_aseg = models.CharField(max_length=255, blank=True, null=True)
    af_num_poliza_seguro = models.CharField(max_length=255, blank=True, null=True)
    poliza_vigencia = models.DateField(blank=True, null=True)
    facturista = models.ForeignKey(FacturistaEmbarques, models.DO_NOTHING)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=100, blank=True, null=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()
    numero_serie = models.CharField(max_length=255, blank=True, null=True)
    imei = models.CharField(max_length=50, blank=True, null=True)
    sucursal = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'transporte_embarques'

class Operador(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.BooleanField(default= False)
    num_licencia = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    comision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    precio_tonelada = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    celular = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    facturista = models.ForeignKey(FacturistaEmbarques, models.DO_NOTHING, blank=True, null=True)
    transporte = models.ForeignKey(TransporteEmbarques, models.DO_NOTHING, blank=True, null=True)
    sx = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=100, blank=True, null=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='operador')

    objects = OperadorManager()

    class Meta:
        managed = True
        db_table = 'operador'

class CpOperador(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.TextField()  # This field type is a guess.
    operador = models.OneToOneField(Operador, models.DO_NOTHING)
    cve_transporte = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13)
    direccion_calle = models.CharField(max_length=200, blank=True, null=True)
    direccion_numero_exterior = models.CharField(max_length=50, blank=True, null=True)
    direccion_numero_interior = models.CharField(max_length=50, blank=True, null=True)
    direccion_codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=255, blank=True, null=True)
    direccion_municipio = models.CharField(max_length=255, blank=True, null=True)
    direccion_estado = models.CharField(max_length=255, blank=True, null=True)
    direccion_pais = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'cp_operador'


class CpTransporte(models.Model):
    id = models.BigAutoField(primary_key=True)
    transporte = models.OneToOneField(TransporteEmbarques, models.DO_NOTHING)
    propietario = models.ForeignKey(Propietario, models.DO_NOTHING)
    iv_config_vehicular = models.CharField(max_length=255, blank=True, null=True)
    af_perm_sct = models.CharField(max_length=255, blank=True, null=True)
    af_num_permiso_sct = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'cp_transporte'