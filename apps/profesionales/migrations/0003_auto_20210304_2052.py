# Generated by Django 2.2.8 on 2021-03-04 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0002_auto_20200422_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesional',
            name='apellido',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profesional',
            name='nombre',
            field=models.CharField(max_length=100, null=True),
        ),
    ]