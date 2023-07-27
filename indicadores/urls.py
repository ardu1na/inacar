from django.urls import path
from indicadores import views

urlpatterns = [

    # EMPLEADO
    
    ### ver evaluaciones 
    path('evaluaciones_empleado/',views.evaluaciones_empleado, name="evaluaciones_empleado"),
    
    path('evaluacion/empezar/',views.nueva_evaluacion, name="nueva_evaluacion"),
    path('evaluacion/<int:id>/continuar/',views.evaluacion_competencia, name="evaluacion_competencia"),

 ]