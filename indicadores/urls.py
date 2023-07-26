from django.urls import path
from indicadores import views

urlpatterns = [
    #Administrador
    path('evaluacion/<int:id>/',views.evaluacion, name="evaluacion"),
    path('success/',views.success, name="success"),
    path('evaluaciones_empleado/',views.evaluaciones_empleado, name="evaluaciones_empleado"),


]