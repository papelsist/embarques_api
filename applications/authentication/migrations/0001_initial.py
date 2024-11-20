# Generated by Django 3.2 on 2024-11-19 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('version', models.BigIntegerField(blank=True, default=1, null=True)),
                ('account_expired', models.BooleanField(default=False)),
                ('account_locked', models.BooleanField(default=False)),
                ('nombre', models.CharField(max_length=255)),
                ('nombres', models.CharField(max_length=255)),
                ('puesto', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_de_empleado', models.IntegerField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=255)),
                ('password_expired', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('nip', models.CharField(blank=True, max_length=12, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
