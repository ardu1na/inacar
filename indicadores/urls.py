from django.urls import path
from indicadores import views

urlpatterns = [

    # EMPLEADO
    
    ### ver evaluaciones 
    path('empleado/evaluaciones/',views.evaluaciones_empleado, name="evaluaciones_empleado"),
    
    path('empleado/evaluacion/empezar/',views.nueva_evaluacion, name="nueva_evaluacion"),
    path('empleado/evaluacion/<int:id>/continuar/',views.evaluacion_competencia, name="evaluacion_competencia"),
    
    
    
    # LIDER
    
    ### ver evaluaciones 
    path('lider/evaluaciones/',views.evaluaciones_lider, name="evaluaciones_lider"),
    
    path('lider/evaluacion/<int:id>/',views.responder_evaluacion, name="evaluacion_lider"),
    
    path('lider/evaluacion/<int:id>/continuar/',views.comptencia_lider, name="comptencia_lider"),
    
    

 ]