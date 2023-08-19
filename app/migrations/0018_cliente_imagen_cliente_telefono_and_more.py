# Generated by Django 4.2.2 on 2023-08-19 11:37

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_lote_nro_documento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='imagen',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='/imagen/default_cliente.jpg', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[100, None], upload_to='clientes/'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='/imagen/default.jpg', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[100, None], upload_to='productos/'),
        ),
    ]
