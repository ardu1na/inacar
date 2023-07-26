from django.urls import path
from indicadores import views

urlpatterns = [
    #Administrador
    path('evaluacion/',views.evaluacion, name="test"),
    path('success/',views.success, name="success"),

]