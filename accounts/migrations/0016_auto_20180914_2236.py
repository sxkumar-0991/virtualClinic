# Generated by Django 2.1 on 2018-09-14 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_doctoraddress_patientaddress'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctoraddress',
            options={'ordering': ['doctor']},
        ),
        migrations.AlterModelOptions(
            name='patientaddress',
            options={'ordering': ['patient']},
        ),
        migrations.AlterModelTable(
            name='doctoraddress',
            table='doctor_address',
        ),
        migrations.AlterModelTable(
            name='patientaddress',
            table='patient_address',
        ),
    ]
