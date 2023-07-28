from django.db import models
from datetime import date
from django.contrib.auth.models import User


class NivelAdministrativo(models.Model):
    nombre = models.CharField(max_length=230, null=False)
    def __str__(self):
        return self.nombre
    
class Cargo(models.Model):
    nombre = models.CharField(max_length=230, null=False)
    
    def __str__(self):
        return self.nombre

class Director(models.Model):
    user = models.OneToOneField(User, related_name="director", on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="directores", null=True, blank=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

        
    @property
    def get_nombre(self):
        return self.user.get_full_name

class Lider(models.Model):
    user = models.OneToOneField(User, related_name="lider", on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="lideres", null=True, blank=False)
    nivel_administrativo = models.ForeignKey(
                    NivelAdministrativo, on_delete=models.CASCADE, null=True, related_name="lideres", blank=False
                    )
    director = models.ForeignKey(
                    Director, on_delete=models.CASCADE, null=True, related_name="lideres", blank=False
                    )
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

        
    @property
    def get_nombre(self):
        return self.user.get_full_name

class Empleado(models.Model):
    user = models.OneToOneField(
                User, related_name="empleado", on_delete=models.CASCADE
                )
    cargo = models.ForeignKey(
                    Cargo, on_delete=models.CASCADE, related_name="empleados", null=True, blank=False
                    )
    nivel_administrativo = models.ForeignKey(
                    NivelAdministrativo, on_delete=models.CASCADE, null=True, related_name="empleados", blank=False
                    )
    lider = models.ForeignKey(
                    Lider, on_delete=models.CASCADE, null=True, related_name="empleados", blank=False
                    )
    
    regional = models.ForeignKey(
                    'Regional', related_name="empleados", on_delete=models.SET_NULL, null=True
                    )    

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

#### INFO DE LA EVALUACION
class Regional (models.Model):
    nombre = models.CharField(max_length=150)
    
    def __str__ (self):
        return f'Regional/Operación: {self.nombre}'
    
    class Meta:
        verbose_name = "Regional/Operación"
        verbose_name_plural = "Regionales/Operaciones"
      
#### INSTANCIA DE EVALUACION      
class Evaluacion (models.Model):
    
    
        
    director = models.ForeignKey(
                                Director, related_name="evaluaciones", on_delete=models.SET_NULL, null=True, blank=True)
        
    lider = models.ForeignKey(
                                Lider, related_name="evaluaciones", on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(
                                Empleado, related_name="evaluaciones", on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(
                                default=date.today())
    
    def __str__ (self):
        if self.empleado:
            return f'Evaluación {self.id} de {self.empleado} {self.fecha}'
        else:
            return f'Evaluación {self.id} de {self.lider} {self.fecha}'

        
    class Meta:
        verbose_name_plural = "Evaluaciones"
        
#### TABLA DE OBJETIVOS
class Objetivo (models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=950)
    
    # cada cargo tiene sus propias preguntas de objetivo
    cargo = models.ForeignKey(
            Cargo, related_name = "objetivos", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__ (self):
            return f'{self.nombre}'    
        
class RespuestaObjetivo (models.Model):
    
    objetivo = models.ForeignKey(
                            Objetivo, related_name="respuesta", on_delete=models.CASCADE )
    
    evaluacion = models.ForeignKey(Evaluacion,
                                   related_name="respuestas_objetivo", on_delete=models.CASCADE)
    
    observaciones_evaluado = models.CharField(max_length=950, null=True, blank=True)

    resultado_evaluado = models.IntegerField(null=True, blank=True)
    
    observaciones_evaluador = models.CharField(max_length=950, null=True, blank=True)

    resultado_evaluador = models.IntegerField(null=True, blank=True)
    
    def __str__ (self):
            return f'{self.objetivo}' 
    
    class Meta:
        verbose_name_plural = "Respuestas a los Objetivos"
        verbose_name = "Respuesta al objetivo"   

#### TABLA DE COMPETENCIAS 
class Competencia (models.Model):
    nombre = models.CharField(max_length=150)
    definicion = models.CharField(max_length=950)
    
    nivel_administrativo = models.ForeignKey(
                NivelAdministrativo,
                related_name="competencias",
                on_delete=models.SET_NULL,
                null=True,
                blank=True)
    
    def __str__ (self):
        return f'{self.nombre}'   
    
class Pregunta (models.Model): 
    competencia = models.ForeignKey(Competencia, related_name="preguntas", on_delete=models.SET_NULL, null=True)

    nombre = models.CharField(max_length=150)
    
    def __str__ (self):
        return f'{self.nombre}'
    
    class Meta:
        verbose_name = "Definición"
                    
class RespuestaCompetencia (models.Model):
    evaluacion = models.ForeignKey(
                            Evaluacion, related_name="respuestas_competencia", on_delete=models.SET_NULL, null=True)
    pregunta = models.ForeignKey(
                            Pregunta, related_name="respuestas", on_delete=models.SET_NULL, null=True)
    
    descripcion_empleado = models.CharField(max_length=950, help_text="Descripción del Resultado que soporta la calificación, sobre hechos y datos (ejemplos)", null=True, blank=True)
    
    porcentaje_empleado = models.IntegerField(verbose_name="Porcentaje de desarrollo", help_text="Valor de desarrollo de la competencia", null=True, blank=True)
    
    descripcion_lider = models.CharField(max_length=950, help_text="Descripción del Resultado que soporta la calificación, sobre hechos y datos (ejemplos)", null=True, blank=True)
    
    porcentaje_lider = models.IntegerField(verbose_name="Porcentaje de desarrollo", help_text="Valor de desarrollo de la competencia", null=True, blank=True)
  
  
    def __str__ (self):
        return self.pregunta.competencia.nombre
    
    
    
    class Meta:
        verbose_name_plural = "Respuestas a las Competencias"
        verbose_name = "Respuesta"