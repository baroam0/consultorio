# Generated by Django 2.2.8 on 2020-06-05 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_auto_20200406_0150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pacienteobrasocial',
            old_name='observacion',
            new_name='observaciones',
        ),
    ]