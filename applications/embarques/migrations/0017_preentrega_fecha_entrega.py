# Generated by Django 3.2 on 2024-12-05 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0016_preentrega_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='preentrega',
            name='fecha_entrega',
            field=models.DateField(blank=True, null=True),
        ),
    ]
