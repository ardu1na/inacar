from django.urls import path
from indicadores import views

urlpatterns = [

    path('evaluacion/<int:id>/',views.evaluacion, name="evaluacion"),
    path('evaluacion/',views.evaluacion, name="evaluacion_nueva"),

    path('success/',views.success, name="success"),
    
    path('evaluaciones_empleado/',views.evaluaciones_empleado, name="evaluaciones_empleado"),


]