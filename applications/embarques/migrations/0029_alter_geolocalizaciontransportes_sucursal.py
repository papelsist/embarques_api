# Generated by Django 3.2 on 2024-10-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0028_alter_geolocalizaciontransportes_transporte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocalizaciontransportes',
            name='sucursal',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]