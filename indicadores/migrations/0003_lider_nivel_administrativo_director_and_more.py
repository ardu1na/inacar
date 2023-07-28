# Generated by Django 4.2.1 on 2023-07-28 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indicadores', '0002_competencia_nivel_administrativo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lider',
            name='nivel_administrativo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lideres', to='indicadores.niveladministrativo'),
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directores', to='indicadores.cargo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='directores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='director',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluaciones', to='indicadores.director'),
        ),
        migrations.AddField(
            model_name='lider',
            name='director',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lideres', to='indicadores.director'),
        ),
    ]
