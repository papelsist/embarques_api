# Generated by Django 3.2 on 2024-04-04 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0018_entregaincidenciaseguimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregaincidencia',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
