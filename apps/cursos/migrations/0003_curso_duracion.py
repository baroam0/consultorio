# Generated by Django 2.2 on 2021-07-23 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0002_alumno_curso_modulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='duracion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
