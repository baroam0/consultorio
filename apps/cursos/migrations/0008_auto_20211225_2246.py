# Generated by Django 2.2.8 on 2021-12-26 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0007_auto_20211023_0900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modulo',
            options={'verbose_name_plural': 'Modulos'},
        ),
        migrations.AddField(
            model_name='alumno',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='telefono',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='numerodocumento',
            field=models.IntegerField(unique=True),
        ),
    ]