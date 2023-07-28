from django.contrib import admin
from indicadores.models import RespuestaCompetencia, Pregunta, \
    Competencia, RespuestaObjetivo, Objetivo, Evaluacion,\
    Regional, Empleado, Lider, Cargo, NivelAdministrativo, Director
        
admin.site.register(Empleado)
admin.site.register(RespuestaObjetivo)

class PreguntaInline(admin.StackedInline):
    model = Pregunta
    extra = 0

class RespuestaCompetenciaInline(admin.StackedInline):
    model = RespuestaCompetencia
    extra = 0

class RespuestaObjetivoInline(admin.StackedInline):
    model = RespuestaObjetivo
    extra = 0

class CompetenciaInline(admin.StackedInline):
    model = Competencia
    extra = 0
        
        
class ObjetivoInline(admin.StackedInline):
    model = Objetivo
    extra = 0

class LiderInline(admin.StackedInline):
    model = Lider
    extra = 0
    
            
admin.site.register(Regional)


class CargoAdmin(admin.ModelAdmin):
    inlines = [ObjetivoInline,]
admin.site.register(Cargo, CargoAdmin)



class DirectorAdmin(admin.ModelAdmin):
    inlines = [LiderInline,]
admin.site.register(Director, DirectorAdmin)


class CompetenciaAdmin(admin.ModelAdmin):
    inlines = [PreguntaInline,]
admin.site.register(Competencia, CompetenciaAdmin)


class NivelAdministrativoAdmin(admin.ModelAdmin):
    inlines = [CompetenciaInline,]
admin.site.register(NivelAdministrativo, NivelAdministrativoAdmin)




admin.site.register(Lider)




admin.site.register(Objetivo)


class EvaluacionAdmin(admin.ModelAdmin):
    inlines = [RespuestaCompetenciaInline, RespuestaObjetivoInline]
    list_display=['fecha','get_competencias','get_porcentaje_respuestas_objetivo_evaluado', 'get_porcentaje_respuestas_objetivo_evaluador']
admin.site.register(Evaluacion, EvaluacionAdmin)
