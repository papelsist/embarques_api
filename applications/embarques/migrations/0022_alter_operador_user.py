# Generated by Django 3.2 on 2024-04-11 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('embarques', '0021_entregaincidencia_folio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operador',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='operador', to=settings.AUTH_USER_MODEL),
        ),
    ]