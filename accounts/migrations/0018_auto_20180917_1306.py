# Generated by Django 2.1 on 2018-09-17 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20180917_1304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readings',
            options={'ordering': ['-date_time']},
        ),
    ]