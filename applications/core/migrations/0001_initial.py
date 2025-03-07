# Generated by Django 3.2 on 2024-11-19 17:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.BigIntegerField()),
                ('certificado_digital', models.BinaryField(blank=True, null=True)),
                ('certificado_digital_pfx', models.BinaryField(blank=True, null=True)),
                ('clave', models.CharField(max_length=15, unique=True)),
                ('llave_privada', models.BinaryField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('numero_de_certificado', models.CharField(blank=True, max_length=20, null=True)),
                ('password_pac', models.CharField(blank=True, max_length=255, null=True)),
                ('password_pfx', models.CharField(blank=True, max_length=255, null=True)),
                ('regimen', models.CharField(max_length=300)),
                ('rfc', models.CharField(max_length=13)),
                ('timbrado_de_prueba', models.BooleanField(default=True)),
                ('usuario_pac', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_calle', models.CharField(blank=True, max_length=200, null=True)),
                ('direccion_codigo_postal', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_colonia', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_estado', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_latitud', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('direccion_longitud', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('direccion_municipio', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_numero_exterior', models.CharField(blank=True, max_length=50, null=True)),
                ('direccion_numero_interior', models.CharField(blank=True, max_length=50, null=True)),
                ('direccion_pais', models.CharField(blank=True, max_length=100, null=True)),
                ('regimen_clave_sat', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'empresa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.BigIntegerField(default=0)),
                ('activa', models.BooleanField(default=True)),
                ('clave', models.CharField(max_length=20, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('sw2', models.BigIntegerField(blank=True, null=True)),
                ('direccion_calle', models.CharField(blank=True, max_length=200, null=True)),
                ('direccion_codigo_postal', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_colonia', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_estado', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_latitud', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('direccion_longitud', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('direccion_municipio', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_numero_exterior', models.CharField(blank=True, max_length=50, null=True)),
                ('direccion_numero_interior', models.CharField(blank=True, max_length=50, null=True)),
                ('direccion_pais', models.CharField(blank=True, max_length=100, null=True)),
                ('almacen', models.BooleanField(default=True)),
                ('db_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'sucursal',
                'managed': False,
            },
        ),
    ]
