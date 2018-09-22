# Generated by Django 2.1 on 2018-08-15 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='product_id',
            field=models.CharField(help_text='Unique Product ID of the device.', max_length=4, null=True, unique=True, verbose_name='Product ID'),
        ),
        migrations.AlterField(
            model_name='device',
            name='deviceid',
            field=models.CharField(help_text='Bluetooth pin of the devce.', max_length=7, unique=True, verbose_name='Device ID'),
        ),
    ]
