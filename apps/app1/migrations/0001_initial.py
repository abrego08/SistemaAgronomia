# Generated by Django 2.2.6 on 2020-03-25 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('codigo_expediente', models.IntegerField(primary_key=True, serialize=False)),
                ('apellido_paciente', models.CharField(max_length=50)),
                ('segApellPaciente', models.CharField(max_length=50)),
                ('nombre_paciente', models.CharField(max_length=50)),
                ('segNombrePaciente', models.CharField(max_length=50)),
                ('edad_paciente', models.IntegerField()),
                ('sexo_paciente', models.CharField(max_length=1)),
                ('direccion_paciente', models.CharField(max_length=200)),
                ('telefono_paciente', models.CharField(max_length=8)),
                ('ocupacion_paciente', models.CharField(max_length=50)),
                ('lugar_trabajo_paciente', models.CharField(max_length=100, null=True)),
                ('responsable_paciente', models.CharField(max_length=50)),
                ('fecha_nacimiento_paciente', models.DateField()),
                ('fecha_expediente', models.DateField()),
                ('estado_expediente', models.CharField(max_length=50)),
                ('histoMedica', models.CharField(max_length=300)),
                ('histoOdonto', models.CharField(max_length=300)),
            ],
        ),
    ]
