# Generated by Django 4.2.1 on 2023-07-26 11:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indicadores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='empleado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='fecha',
            field=models.DateField(default=datetime.date(2023, 7, 26)),
        ),
        migrations.AlterField(
            model_name='lider',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lider', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='respuestaobjetivo',
            name='evaluacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='respuestas_objetivo', to='indicadores.evaluacion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='respuestaobjetivo',
            name='objetivo',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='respuesta', to='indicadores.objetivo'),
            preserve_default=False,
        ),
    ]