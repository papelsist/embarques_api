# Generated by Django 3.2 on 2024-04-17 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0022_alter_operador_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregaincidenciaseguimiento',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]