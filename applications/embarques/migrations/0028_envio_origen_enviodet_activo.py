from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("embarques", "0027_direccionentrega_atiende_sabado_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="envio",
            name="envio_origen",
            field=models.ForeignKey(
                blank=True,
                db_column="envio_origen_id",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="envios_hijos",
                to="embarques.envio",
            ),
        ),
        migrations.AddField(
            model_name="enviodet",
            name="activo",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="enviodet",
            name="envio_hijo",
            field=models.ForeignKey(
                blank=True,
                db_column="envio_hijo_id",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="detalles_reasignados_origen",
                to="embarques.envio",
            ),
        ),
    ]
