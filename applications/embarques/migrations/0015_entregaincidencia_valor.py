# Generated by Django 3.2 on 2024-03-12 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0014_auto_20240312_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregaincidencia',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]
