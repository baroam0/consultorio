# Generated by Django 2.2.8 on 2020-04-23 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
