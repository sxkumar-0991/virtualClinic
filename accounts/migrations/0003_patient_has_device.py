# Generated by Django 2.1 on 2018-08-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180815_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='has_device',
            field=models.BooleanField(default=False, verbose_name='Has Device'),
        ),
    ]