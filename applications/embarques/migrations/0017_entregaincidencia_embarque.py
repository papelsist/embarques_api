# Generated by Django 3.2 on 2024-03-12 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0016_auto_20240312_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregaincidencia',
            name='embarque',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
