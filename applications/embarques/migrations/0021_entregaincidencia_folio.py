# Generated by Django 3.2 on 2024-04-04 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0020_alter_entregaincidenciaseguimiento_incidencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregaincidencia',
            name='folio',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]