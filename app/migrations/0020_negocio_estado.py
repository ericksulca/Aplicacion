# Generated by Django 4.2.2 on 2023-08-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_negocio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='negocio',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
