# Generated by Django 4.2.2 on 2023-08-10 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_insumo_presentacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto_presentacions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_compra', models.FloatField(blank=True, default=0)),
                ('precio_venta', models.FloatField(blank=True, default=0)),
                ('valor', models.FloatField(blank=True, default=1)),
                ('favorito', models.BooleanField(blank=True, default=False)),
                ('estado', models.BooleanField(blank=True, default=True)),
                ('presentacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.presentacion')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
    ]
