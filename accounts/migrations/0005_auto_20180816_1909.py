# Generated by Django 2.1 on 2018-08-16 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180816_1907'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='device',
            table='device',
        ),
        migrations.AlterModelTable(
            name='patient',
            table='patient',
        ),
        migrations.AlterModelTable(
            name='readings',
            table='readings',
        ),
        migrations.AlterModelTable(
            name='relative',
            table='relative',
        ),
    ]