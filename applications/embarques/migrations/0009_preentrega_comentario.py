# Generated by Django 3.2 on 2024-12-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embarques', '0008_auto_20241202_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='preentrega',
            name='comentario',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]