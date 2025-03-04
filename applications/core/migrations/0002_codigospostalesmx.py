# Generated by Django 3.2 on 2024-12-03 12:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigosPostalesMX',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('estado', models.CharField(blank=True, max_length=255, null=True)),
                ('asentamiento', models.CharField(blank=True, max_length=255, null=True)),
                ('codigo', models.CharField(blank=True, max_length=255, null=True)),
                ('colonia', models.CharField(blank=True, max_length=255, null=True)),
                ('municipio', models.CharField(blank=True, max_length=255, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=255, null=True)),
                ('municipio_sat', models.CharField(blank=True, max_length=255, null=True)),
                ('localidad_sat', models.CharField(blank=True, max_length=255, null=True)),
                ('codigo_sat', models.CharField(blank=True, max_length=255, null=True)),
                ('estado_sat', models.CharField(blank=True, max_length=255, null=True)),
                ('pais', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'codigos_postales_mx',
                'managed': True,
            },
        ),
    ]
