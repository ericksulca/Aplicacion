# Generated by Django 4.2.2 on 2023-08-25 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_aperturacaja_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aperturacaja',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]