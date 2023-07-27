from django.urls import path
from indicadores import views

urlpatterns = [

    # EMPLEADO
    
    ### ver evaluaciones 
    path('evaluaciones_empleado/',views.evaluaciones_empleado, name="evaluaciones_empleado"),
    
    path('evaluacion/empezar/',views.nueva_evaluacion, name="nueva_evaluacion"),
    path('evaluacion/<int:id>/continuar/',views.evaluacion_competencia, name="evaluacion_competencia"),
    
    
    
    # LIDER
    
    ### ver evaluaciones 
    path('evaluaciones_lider/',views.evaluaciones_lider, name="evaluaciones_lider"),
    
    path('evaluacion/<int:id>/',views.responder_evaluacion, name="evaluacion_lider"),
    
    path('evaluacion/<int:id>/continuar/',views.evaluacion_competencia_lider, name="evaluacion_competencia_lider"),
    
    

 ]