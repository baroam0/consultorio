# Generated by Django 2.2.8 on 2020-04-27 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bancos', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Titular',
        ),
        migrations.AlterField(
            model_name='datosbancarios',
            name='titular',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
