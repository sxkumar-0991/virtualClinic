# Generated by Django 2.1 on 2018-08-17 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180816_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='patient',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.Patient'),
        ),
    ]
