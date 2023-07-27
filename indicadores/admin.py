from django.contrib import admin
from indicadores.models import RespuestaCompetencia, Pregunta, \
    Competencia, RespuestaObjetivo, Objetivo, Evaluacion,\
    Regional, Empleado, Lider, Cargo, NivelAdministrativo
        
admin.site.register(Empleado)
admin.site.register(Cargo)
admin.site.register(RespuestaObjetivo)
admin.site.register(NivelAdministrativo)

class PreguntaInline(admin.StackedInline):
    model = Pregunta
    extra = 0

class RespuestaCompetenciaInline(admin.StackedInline):
    model = RespuestaCompetencia
    extra = 0

class RespuestaObjetivoInline(admin.StackedInline):
    model = RespuestaObjetivo
    extra = 0

        
admin.site.register(Regional)

class CompetenciaAdmin(admin.ModelAdmin):
    inlines = [PreguntaInline,]
admin.site.register(Competencia, CompetenciaAdmin)



admin.site.register(Lider)




admin.site.register(Objetivo)


class EvaluacionAdmin(admin.ModelAdmin):
    inlines = [RespuestaCompetenciaInline, RespuestaObjetivoInline]
admin.site.register(Evaluacion, EvaluacionAdmin)
