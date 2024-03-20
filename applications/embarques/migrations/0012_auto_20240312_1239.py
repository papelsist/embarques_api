# Generated by Django 3.2 on 2024-03-12 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0011_alter_entregaincidencia_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entregaincidencia',
            name='area',
        ),
        migrations.RemoveField(
            model_name='entregaincidencia',
            name='completo',
        ),
        migrations.RemoveField(
            model_name='entregaincidencia',
            name='reporto_nombre',
        ),
        migrations.RemoveField(
            model_name='entregaincidencia',
            name='reporto_puesto',
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='clave',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='descripcion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='devuelto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='envio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='incidencias', to='embarques.envio'),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='img1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='img2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='img3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='entregaincidencia',
            name='incompleto',
            field=models.BooleanField(default=False),
        )
    ]
