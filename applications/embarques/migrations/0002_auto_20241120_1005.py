# Generated by Django 3.2 on 2024-11-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='envio',
            name='de_destino',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='envio',
            name='de_rfc_destinatario',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='envio',
            name='email_envio',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='envio',
            name='maniobra',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
    ]
