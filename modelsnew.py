# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CpCfdi(models.Model):
    id = models.BigAutoField(primary_key=True)
    embarque = models.ForeignKey('Embarques', models.DO_NOTHING)
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
        managed = False
        db_table = 'cp_cfdi'


class CpEmbarques(models.Model):
    id = models.BigAutoField(primary_key=True)
    embarque = models.OneToOneField('Embarques', models.DO_NOTHING)
    cp_version = models.CharField(max_length=20, blank=True, null=True)
    cp_transp_internac = models.CharField(max_length=20, blank=True, null=True)
    cp_total_distancia_recorrida = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    or_origen = models.CharField(max_length=20, blank=True, null=True)
    or_rfc_remitente = models.CharField(max_length=255)
    or_cliente_remitente = models.CharField(max_length=255, blank=True, null=True)
    me_unidad_peso = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()
    cliente = models.ForeignKey('Empresa', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cp_embarques'


class CpEnvio(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.OneToOneField('Envio', models.DO_NOTHING)
    de_destino = models.CharField(max_length=20, blank=True, null=True)
    de_rfc_destinatario = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cp_envio'


class CpEnvioDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio_det_id = models.BigIntegerField(unique=True)
    me_bienes_transp = models.CharField(max_length=255, blank=True, null=True)
    me_clave_unidad = models.CharField(max_length=255, blank=True, null=True)
    me_material_peligroso = models.CharField(max_length=2, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cp_envio_det'


class CpFacturista(models.Model):
    id = models.BigAutoField(primary_key=True)
    facturista = models.OneToOneField('FacturistaEmbarques', models.DO_NOTHING)
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
        managed = False
        db_table = 'cp_facturista'


class CpInstruccionDeEnvio(models.Model):
    id = models.BigAutoField(primary_key=True)
    instruccion = models.OneToOneField('InstruccionDeEnvio', models.DO_NOTHING)
    ub_distancia_recorrida = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    de_fecha_hora_progllegada = models.DateTimeField(blank=True, null=True)
    version = models.BigIntegerField()
    de_municipio = models.CharField(max_length=255, blank=True, null=True)
    de_estado = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cp_instruccion_de_envio'


class CpOperador(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.TextField()  # This field type is a guess.
    operador = models.OneToOneField('Operador', models.DO_NOTHING)
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
        managed = False
        db_table = 'cp_operador'


class CpTransporte(models.Model):
    id = models.BigAutoField(primary_key=True)
    transporte = models.OneToOneField('TransporteEmbarques', models.DO_NOTHING)
    propietario = models.ForeignKey('Propietario', models.DO_NOTHING)
    iv_config_vehicular = models.CharField(max_length=255, blank=True, null=True)
    af_perm_sct = models.CharField(max_length=255, blank=True, null=True)
    af_num_permiso_sct = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cp_transporte'


class Embarques(models.Model):
    id = models.BigAutoField(primary_key=True)
    documento = models.IntegerField(blank=True, null=True)
    operador = models.ForeignKey('Operador', models.DO_NOTHING)
    sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING)
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
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()
    cp = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'embarques'


class Empresa(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField()
    certificado_digital = models.TextField(blank=True, null=True)
    certificado_digital_pfx = models.TextField(blank=True, null=True)
    clave = models.CharField(max_length=15)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    llave_privada = models.TextField(blank=True, null=True)
    nombre = models.CharField(max_length=255)
    numero_de_certificado = models.CharField(max_length=20, blank=True, null=True)
    password_pac = models.CharField(max_length=255, blank=True, null=True)
    password_pfx = models.CharField(max_length=255, blank=True, null=True)
    regimen = models.CharField(max_length=300)
    rfc = models.CharField(unique=True, max_length=13)
    timbrado_de_prueba = models.TextField()  # This field type is a guess.
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

    class Meta:
        managed = False
        db_table = 'empresa'


class Entrega(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.ForeignKey('Envio', models.DO_NOTHING)
    embarque = models.ForeignKey(Embarques, models.DO_NOTHING)
    sucursal = models.CharField(max_length=255)
    destinatario = models.CharField(max_length=255, blank=True, null=True)
    operador = models.CharField(max_length=255, blank=True, null=True)
    origen = models.CharField(max_length=255)
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
    arribo_latitud = models.DecimalField(max_digits=19, decimal_places=2)
    arribo_longitud = models.DecimalField(max_digits=19, decimal_places=2)
    recepcion = models.DateTimeField(blank=True, null=True)
    recepcion_latitud = models.DecimalField(max_digits=19, decimal_places=2)
    recepcion_longitud = models.DecimalField(max_digits=19, decimal_places=2)
    regreso = models.DateTimeField(blank=True, null=True)
    recibio = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    reporto_nombre = models.CharField(max_length=255, blank=True, null=True)
    reporto_puesto = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'entrega'


class EntregaComision(models.Model):
    id = models.BigAutoField(primary_key=True)
    entrega = models.ForeignKey(Entrega, models.DO_NOTHING)
    valor = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    valor_caja = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    precio_tonelada = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    maniobra = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    importe_comision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    comision_por_tonelada = models.TextField()  # This field type is a guess.
    comentario_comision = models.CharField(max_length=255, blank=True, null=True)
    fecha_comision = models.DateTimeField(blank=True, null=True)
    manual = models.TextField()  # This field type is a guess.
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'entrega_comision'


class EntregaDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    entrega = models.ForeignKey(Entrega, models.DO_NOTHING)
    envio_det = models.ForeignKey('EnvioDet', models.DO_NOTHING)
    sx_instruccion_de_envio = models.CharField(max_length=255, blank=True, null=True)
    almacen = models.CharField(max_length=255, blank=True, null=True)
    instruccion_de_entrega_parcial = models.CharField(max_length=255, blank=True, null=True)
    clave = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=19, decimal_places=2)
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'entrega_det'


class EntregaIncidencia(models.Model):
    id = models.BigAutoField(primary_key=True)
    entrega_det = models.ForeignKey(EntregaDet, models.DO_NOTHING)
    entregado = models.TextField()  # This field type is a guess.
    incompleto = models.DecimalField(max_digits=19, decimal_places=2)
    devuelto = models.DecimalField(max_digits=19, decimal_places=2)
    maltratado = models.TextField()  # This field type is a guess.
    impreso = models.TextField()  # This field type is a guess.
    cortado = models.TextField()  # This field type is a guess.
    motivo = models.CharField(max_length=255, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrega_incidencia'


class Envio(models.Model):
    id = models.BigAutoField(primary_key=True)
    sucursal = models.CharField(max_length=255)
    origen = models.CharField(max_length=255)
    entidad = models.CharField(max_length=255)
    fecha_documento = models.DateTimeField()
    documento = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=255)
    forma_pago = models.CharField(max_length=255, blank=True, null=True)
    pagado = models.TextField()  # This field type is a guess.
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

    class Meta:
        managed = False
        db_table = 'envio'


class EnvioDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.ForeignKey(Envio, models.DO_NOTHING)
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

    class Meta:
        managed = False
        db_table = 'envio_det'


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
        managed = False
        db_table = 'facturista_embarques'


class InstruccionDeEnvio(models.Model):
    id = models.BigAutoField(primary_key=True)
    envio = models.ForeignKey(Envio, models.DO_NOTHING)
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
    direccion_latitud = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    direccion_longitud = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    fecha_de_entrega = models.DateTimeField(blank=True, null=True)
    sx = models.CharField(unique=True, max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'instruccion_de_envio'


class Operador(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.TextField()  # This field type is a guess.
    num_licencia = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    comision = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    precio_tonelada = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    celular = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    facturista = models.ForeignKey(FacturistaEmbarques, models.DO_NOTHING)
    transporte = models.ForeignKey('TransporteEmbarques', models.DO_NOTHING)
    sx = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=100, blank=True, null=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'operador'


class Propietario(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.TextField()  # This field type is a guess.
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
        managed = False
        db_table = 'propietario'


class Sucursal(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.TextField()  # This field type is a guess.
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
    almacen = models.TextField()  # This field type is a guess.
    db_url = models.CharField(max_length=255, blank=True, null=True)
    sx = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    create_user = models.CharField(max_length=100, blank=True, null=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    version = models.BigIntegerField()
    or_municipio = models.CharField(max_length=255, blank=True, null=True)
    or_estado = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sucursal'


class TransporteEmbarques(models.Model):
    id = models.BigAutoField(primary_key=True)
    activo = models.TextField()  # This field type is a guess.
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

    class Meta:
        managed = False
        db_table = 'transporte_embarques'


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
    direccion_latitud = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    direccion_longitud = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    telefono3 = models.CharField(max_length=255, blank=True, null=True)
    telefono2 = models.CharField(max_length=255, blank=True, null=True)
    telefono1 = models.CharField(max_length=255, blank=True, null=True)
    sucursal = models.CharField(max_length=255, blank=True, null=True)
    sx = models.CharField(max_length=255, blank=True, null=True)
    version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'transporte_foraneo'
