# Generated by Django 4.0.6 on 2025-01-04 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
