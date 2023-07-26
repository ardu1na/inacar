from django.shortcuts import render
from indicadores.models import Evaluacion, User, Objetivo, RespuestaObjetivo
from django.contrib.auth.decorators import login_required 
from indicadores.forms import RespuestaObjetivoEmpleadoForm
from django.http import HttpResponse


@login_required
def evaluacion_empleado(request):
    
    empleado = request.user.empleado
    evaluacion = Evaluacion.objects.create(
            empleado=empleado,
    )
    
    for objetivo in empleado.cargo.objetivos.all():
        respuesta_vacia = RespuestaObjetivo.objects.create(
            evaluacion = evaluacion,
            objetivo = objetivo,
            
        )
        
    if request == 'GET':
        for respuesta in evaluacion.respuestas_objetivo.all():
            objetivo = 
        
    
    
    return HttpResponse(f'{evaluacion}')