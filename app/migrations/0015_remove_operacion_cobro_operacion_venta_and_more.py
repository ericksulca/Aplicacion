# Generated by Django 4.2.2 on 2023-08-16 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_rename_fecha_lote_productopresentacions_fecha_caducidad_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operacion',
            name='cobro',
        ),
        migrations.AddField(
            model_name='operacion',
            name='venta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.venta'),
        ),
        migrations.AlterField(
            model_name='cierrecaja',
            name='aperturacaja',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apertura_cierrecaja', to='app.aperturacaja'),
        ),
    ]
