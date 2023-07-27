# Generated by Django 4.2.1 on 2023-07-27 12:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=230)),
            ],
        ),
        migrations.CreateModel(
            name='Competencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('definicion', models.CharField(max_length=950)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empleados', to='indicadores.cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date(2023, 7, 27))),
                ('empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluaciones', to='indicadores.empleado')),
            ],
            options={
                'verbose_name_plural': 'Evaluaciones',
            },
        ),
        migrations.CreateModel(
            name='NivelAdministrativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=230)),
            ],
        ),
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=950)),
                ('cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objetivos', to='indicadores.cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('competencia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preguntas', to='indicadores.competencia')),
            ],
            options={
                'verbose_name': 'Definición',
            },
        ),
        migrations.CreateModel(
            name='Regional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Regional/Operación',
                'verbose_name_plural': 'Regionales/Operaciones',
            },
        ),
        migrations.CreateModel(
            name='RespuestaObjetivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observaciones_empleado', models.CharField(blank=True, max_length=950, null=True)),
                ('resultado_empleado', models.IntegerField(blank=True, null=True)),
                ('observaciones_lider', models.CharField(blank=True, max_length=950, null=True)),
                ('resultado_lider', models.IntegerField(blank=True, null=True)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas_objetivo', to='indicadores.evaluacion')),
                ('objetivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuesta', to='indicadores.objetivo')),
            ],
            options={
                'verbose_name': 'Respuesta al objetivo',
                'verbose_name_plural': 'Respuestas a los Objetivos',
            },
        ),
        migrations.CreateModel(
            name='RespuestaCompetencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_empleado', models.CharField(blank=True, help_text='Descripción del Resultado que soporta la calificación, sobre hechos y datos (ejemplos)', max_length=950, null=True)),
                ('porcentaje_empleado', models.IntegerField(blank=True, help_text='Valor de desarrollo de la competencia', null=True, verbose_name='Porcentaje de desarrollo')),
                ('descripcion_lider', models.CharField(blank=True, help_text='Descripción del Resultado que soporta la calificación, sobre hechos y datos (ejemplos)', max_length=950, null=True)),
                ('porcentaje_lider', models.IntegerField(blank=True, help_text='Valor de desarrollo de la competencia', null=True, verbose_name='Porcentaje de desarrollo')),
                ('evaluacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='respuestas_competencia', to='indicadores.evaluacion')),
                ('pregunta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='respuestas', to='indicadores.pregunta')),
            ],
            options={
                'verbose_name': 'Respuesta',
                'verbose_name_plural': 'Respuestas a las Competencias',
            },
        ),
        migrations.CreateModel(
            name='Lider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lideres', to='indicadores.cargo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='lider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluaciones', to='indicadores.lider'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='lider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empleados', to='indicadores.lider'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='nivel_administrativo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empleados', to='indicadores.niveladministrativo'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='regional',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='empleados', to='indicadores.regional'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='empleado', to=settings.AUTH_USER_MODEL),
        ),
    ]
