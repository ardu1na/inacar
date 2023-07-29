from django.db import models
from datetime import date
from django.contrib.auth.models import User
from decimal import Decimal


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





class InformeAnual(models.Model):
    

    director = models.ForeignKey(
                                Director, related_name="informes_anuales", on_delete=models.SET_NULL, null=True, blank=True)
        
    lider = models.ForeignKey(
                                Lider, related_name="informes_anuales", on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(
                                'Empleado', related_name="informes_anuales", on_delete=models.SET_NULL, null=True, blank=True)
    
    periodo = models.DateField(default=date.today(), verbose_name="año")
            
    resultado = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    
    def __str__ (self):
        
        if self.empleado:
            return f'Informe anual {self.periodo.year} de {self.empleado}'
        else:
            return f'Informe anual {self.periodo.year} de {self.lider}'

        
    class Meta:
        verbose_name_plural = "Informes Anuales"
    
    def save(self, *args, **kwargs):
        if self.pk != None:
            self.resultado = self.get_final_total
        
        super().save(*args, **kwargs)  
    
    @property
    def get_final_total(self):
        evaluaciones = self.evaluaciones.all()
        total = 0
        n_evaluaciones = 0
        if evaluaciones != None:
            for evaluacion in evaluaciones:
                if evaluacion.resultado_final != 0:
                    total += evaluacion.resultado_final
                    n_evaluaciones += 1
            resultado = total / n_evaluaciones
            return resultado
        else:
            return None
        
        ### ahora hacer que uno se guarde con el otro
        
        
        
        
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
    informe_anual = models.ForeignKey(InformeAnual, on_delete=models.CASCADE, null=True, blank=True, related_name="evaluaciones")
   
    director = models.ForeignKey(
                                Director, related_name="evaluaciones", on_delete=models.SET_NULL, null=True, blank=True)
        
    lider = models.ForeignKey(
                                Lider, related_name="evaluaciones", on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(
                                Empleado, related_name="evaluaciones", on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(
                                default=date.today())
    
    porcentaje_objetivos_evaluado = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    porcentaje_objetivos_evaluador = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    
    porcentaje_competencias_evaluado = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    porcentaje_competencias_evaluador = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    
    resultado_final = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    
    
    # RESULTADO FINAL TOTAL: %80 objetivos %20 compentecias
    @property
    def get_final_total(self):
        objetivos = self.respuestas_objetivo.all()
        print(objetivos)
        if objetivos != None:
            if self.porcentaje_objetivos_evaluador != 0:
                objetivos = self.porcentaje_objetivos_evaluador * Decimal(0.8)
            else:
                objetivos = 0
            if self.porcentaje_competencias_evaluador != 0:
                competencias = self.porcentaje_competencias_evaluador * Decimal(0.3)
            else: 
                competencias = 0
            
            return ( objetivos + competencias )/2
        else:
            return self.porcentaje_competencias_evaluador
    
    
    def save(self, *args, **kwargs):
        try:
            self.resultado_final=self.get_final_total
        except:
            pass
        try:
            self.porcentaje_objetivos_evaluado = self.get_porcentaje_respuestas_objetivo_evaluado
        except:
            pass
        try:
            self.porcentaje_objetivos_evaluador = self.get_porcentaje_respuestas_objetivo_evaluador
        except:
            pass
        try:
            self.porcentaje_competencias_evaluado = self.get_porcentaje_competencias_evaluado
        except:
            pass
        try:
            self.porcentaje_competencias_evaluador = self.get_porcentaje_competencias_evaluador
        except:
            pass
        
        
        super().save(*args, **kwargs)  
        
        
        
    def __str__ (self):
        if self.empleado:
            return f'Evaluación {self.id} de {self.empleado} {self.fecha}'
        else:
            return f'Evaluación {self.id} de {self.lider} {self.fecha}'

        
    class Meta:
        verbose_name_plural = "Evaluaciones"
        
    @property
    def get_competencias(self):
        competencias = []
        for respuesta in self.respuestas_competencia.all():
            if respuesta.pregunta.competencia not in competencias:
                competencias.append(respuesta.pregunta.competencia)
        return competencias
    
    @property
    def get_subcompetencias(self):
        subcompetencias = []
        for respuesta in self.respuestas_competencia.all():
            if respuesta.pregunta not in subcompetencias:
                subcompetencias.append(respuesta.pregunta)
        return 
    

    @property
    def get_porcentaje_competencias_evaluado(self):
        
        total_porcentaje = 0
        total_respuestas = 0

        competencias = self.get_competencias
        subcompetencias = self.get_subcompetencias
        
        for competencia in competencias:
            
            competencia_total = 0
            n_respuestas = 0
            
            compe_subcompetencias = []
            for sub in subcompetencias:
                if sub.competencia == competencia:
                    compe_subcompetencias.append(sub)
            
            
            for subcompetencia in compe_subcompetencias:
                
                for respuesta in self.respuestas_competencia.filter(pregunta=subcompetencia):
                    if respuesta.porcentaje_evaluado is not None:
                        competencia_total += respuesta.porcentaje_evaluado
                        n_respuestas += 1

            if n_respuestas > 0:
                competencia_promedio = competencia_total / n_respuestas
                
                total_porcentaje += competencia_promedio
                total_respuestas += 1


        if total_respuestas == 0:
            return 0
        return total_porcentaje / total_respuestas


   
    @property
    def get_porcentaje_competencias_evaluador(self):
        
        total_porcentaje = 0
        total_respuestas = 0

        competencias = self.get_competencias
        subcompetencias = self.get_subcompetencias
        
        for competencia in competencias:
            
            competencia_total = 0
            n_respuestas = 0
            
            compe_subcompetencias = []
            for sub in subcompetencias:
                if sub.competencia == competencia:
                    compe_subcompetencias.append(sub)
            
            
            for subcompetencia in compe_subcompetencias:
                
                for respuesta in self.respuestas_competencia.filter(pregunta=subcompetencia):
                    if respuesta.porcentaje_evaluador is not None:
                        competencia_total += respuesta.porcentaje_evaluador
                        n_respuestas += 1

            if n_respuestas > 0:
                competencia_promedio = competencia_total / n_respuestas
                
                total_porcentaje += competencia_promedio
                total_respuestas += 1


        if total_respuestas == 0:
            return 0

        return total_porcentaje / total_respuestas




        
    @property
    def get_porcentaje_respuestas_objetivo_evaluado(self):
        
        objetivo_total=0
        n_respuestas = 0
        
    
    
    
        respuestas_objetivo = RespuestaObjetivo.objects.filter(evaluacion=self)
        
        for respuesta in respuestas_objetivo:
            if respuesta.resultado_evaluado == None:
                pass
            if respuesta.resultado_evaluado == 0:
                pass
            else:
                objetivo_total  += respuesta.resultado_evaluado
                n_respuestas +=1
                
                
        if objetivo_total == 0 or n_respuestas == 0:
            return None
        
        porcentaje_total = (objetivo_total / n_respuestas) 
    
        return porcentaje_total



     
        
    @property
    def get_porcentaje_respuestas_objetivo_evaluador(self):
        
       
        objetivo_total=0
        n_respuestas = 0
        
    
    
    
        respuestas_objetivo = RespuestaObjetivo.objects.filter(evaluacion=self)
        
        for respuesta in respuestas_objetivo:
            if respuesta.resultado_evaluador == None:
                pass
            if respuesta.resultado_evaluador == 0:
                pass
            else:
                objetivo_total  += respuesta.resultado_evaluador
                n_respuestas +=1
                
                
        if objetivo_total == 0 or n_respuestas == 0:
            return None
        
        porcentaje_total = (objetivo_total / n_respuestas) 
    
        return porcentaje_total
        #### cuando lo quieras renderizar en el template pones:{{evaluacion.get_porcentaje_respuestas_objetivo_evaluador|floatformat:2}}        
            


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
    
    descripcion_evaluado = models.CharField(max_length=950, help_text="Descripción del Resultado que soporta la calificación, sobre hechos y datos (ejemplos)", null=True, blank=True)
    
    porcentaje_evaluado = models.IntegerField(verbose_name="Porcentaje de desarrollo", help_text="Valor de desarrollo de la competencia", null=True, blank=True)
    
    descripcion_evaluador = models.CharField(max_length=950, help_text="Descripción del Resultado que soporta la calificación, sobre hechos y datos (ejemplos)", null=True, blank=True)
    
    porcentaje_evaluador = models.IntegerField(verbose_name="Porcentaje de desarrollo", help_text="Valor de desarrollo de la competencia", null=True, blank=True)
  
    def __str__ (self):
        return self.pregunta.competencia.nombre   
    
    class Meta:
        verbose_name_plural = "Respuestas a las Competencias"
        verbose_name = "Respuesta"
        
        
        
        
        
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
