# Generated by Django 2.2 on 2020-06-11 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pacientes', '0003_auto_20200604_2320'),
        ('profesionales', '0002_auto_20200422_2228'),
        ('obrassociales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechahora', models.DateTimeField()),
                ('asistio', models.BooleanField(default=False)),
                ('entrega', models.BooleanField(default=False)),
                ('entrega_parcial', models.BooleanField(default=False)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('obrasocial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obrassociales.ObraSocial')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.Paciente')),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profesionales.Profesional')),
            ],
            options={
                'verbose_name_plural': 'Turnos',
            },
        ),
    ]
