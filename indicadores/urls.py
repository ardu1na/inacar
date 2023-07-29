from django.urls import path
from indicadores import views

urlpatterns = [

    # EMPLEADO
    
    ### ver evaluaciones 
    path('empleado/evaluaciones/',views.evaluaciones_empleado, name="evaluaciones_empleado"),
    path('empleado/evaluacion/<int:id>/ver/',views.ver_evaluacion_empleado, name="ver_evaluacion_empleado"),

    path('empleado/evaluacion/empezar/',views.nueva_evaluacion, name="nueva_evaluacion"),
    path('empleado/evaluacion/<int:id>/continuar/',views.evaluacion_competencia, name="evaluacion_competencia"),
    
    
    
    # LIDER
    
    ###  evaluaciones a los empleados
    path('lider/empleados/evaluaciones/',views.evaluaciones_lider, name="evaluaciones_lider"),
    
    path('lider/evaluacion/<int:id>/',views.responder_evaluacion, name="evaluacion_lider"),
    
    path('lider/evaluacion/<int:id>/continuar/',views.evaluacion_competencia_lider, name="evaluacion_competencia_lider"),
    
    ###  evaluaciones a si mismo
        
    path('lider/evaluaciones/',views.lider_evaluaciones, name="lider_evaluaciones"),
    
    path('lider/evaluacion/empezar/',views.lider_nueva_evaluacion, name="lider_nueva_evaluacion"),
    
    path('lider/evaluacion/<int:id>/terminar/',views.lider_evaluacion_competencia, name="lider_evaluacion_competencia"),
    
    
    # DIRECTOR
    
    ###  evaluaciones a los lideres
    path('director/evaluaciones/',views.director_evaluaciones, name="director_evaluaciones"),
    
    path('director/evaluacion/<int:id>/',views.evaluar_lider, name="evaluar_lider"),
    
    path('director/evaluacion/<int:id>/continuar/',views.evaluacion_competencia_director, name="evaluacion_competencia_director"),
 ]