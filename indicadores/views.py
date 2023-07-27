from django.shortcuts import render, redirect
from indicadores.models import Evaluacion, RespuestaObjetivo, \
    Competencia, Pregunta, RespuestaCompetencia
from django.contrib.auth.decorators import login_required 
from indicadores.forms import RespuestaObjetivoEmpleadoForm, RespuestaObjetivoLiderForm, \
    RespuestaCompetenciaEmpleadoForm, RespuestaCompetenciaLiderForm
from django.http import HttpResponse
from django.urls import reverse


@login_required
def evaluaciones_empleado(request):
    empleado = request.user.empleado
    evaluaciones = Evaluacion.objects.filter(empleado=empleado)
    context = {
        'empleado': empleado,
        'evaluaciones': evaluaciones,
    }

    template_name = 'indicadores/evaluaciones_empleado.html'
    return render(request, template_name, context)
    
    
    

@login_required # si es operativo que  no muestre objetivos sino competencias
def nueva_evaluacion(request):

    empleado = request.user.empleado

    ## si el empleado tiene objetivos asociados
    objetivos = empleado.cargo.objetivos.all() 
    if objetivos:
        ## crear nueva evaluacion con formulario de objetivos
        evaluacion = Evaluacion.objects.create(empleado=empleado, lider=empleado.lider)

        ### formulario de objetivos para el cargo del empleado
        forms_objetivo = [] 
        for objetivo in objetivos:
            form_objetivo = RespuestaObjetivoEmpleadoForm(request.POST or None, prefix=f'objetivo_{objetivo.pk}')
            forms_objetivo.append((objetivo, form_objetivo))
            
        if 'objetivo' in request.POST:
            for objetivo, form_objetivo in forms_objetivo:
                form_objetivo = RespuestaObjetivoEmpleadoForm(request.POST, prefix=f'objetivo_{objetivo.pk}')
                if form_objetivo.is_valid():
                    respuesta = form_objetivo.save(commit=False) # que hace esto, lo preguarda para
                    respuesta.objetivo = objetivo # asociarloo al objetivo
                    respuesta.evaluacion = evaluacion # asociarlo a la evaluacion
                    respuesta.save() #  y ahora si lo guarda posta.
            return redirect('evaluacion_competencia', id=evaluacion.id)
            
                
            """            
            AQUI hay que redirecionar al empleado al fomrulario de comptenencias que es otra vista
            
            """
        context = {
            'empleado': empleado,
            'forms_objetivo':forms_objetivo,          
        }
    
    else:         
        ## si el empleado NO TIENE objetivos asociados       
        
        ## crear evaluacion solamente de CCOMPETENCIAS
        evaluacion = Evaluacion.objects.create(empleado=empleado, lider=empleado.lider)
        
        ######## formularios de comptencias get
        preguntas = Pregunta.objects.all()
        forms_competencia = []
        for pregunta in preguntas:
            form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
            forms_competencia.append((pregunta, form_competencia))
        
        if 'competencia' in request.POST:
            for pregunta, form_competencia in forms_competencia:
                form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST, prefix=f'pregunta_{pregunta.pk}')
                if form_competencia.is_valid():
                    respuesta = form_competencia.save(commit=False) # que hace esto, lo preguarda para
                    respuesta.pregunta = pregunta # asociarloo a la pregunta
                    respuesta.evaluacion = evaluacion # asociarlo a la evaluacion
                    respuesta.save() #  y ahora si lo guarda posta.
            return redirect('evaluaciones_empleado')
            
        context = {
                'empleado': empleado,
                'forms_comptencia':forms_competencia,          
            }

    template_name = 'indicadores/evaluacion_empleado.html'
    return render(request, template_name, context)

@login_required
def evaluacion_competencia(request, id):
    empleado = request.user.empleado
    evaluacion = Evaluacion.objects.get(id=id)
    preguntas = Pregunta.objects.all()
    forms_competencia = []
    for pregunta in preguntas:
        form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
        forms_competencia.append((pregunta, form_competencia))
    
    if 'competencia' in request.POST:
        for pregunta, form_competencia in forms_competencia:
            form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST, prefix=f'pregunta_{pregunta.pk}')
            if form_competencia.is_valid():
                respuesta = form_competencia.save(commit=False) # que hace esto, lo preguarda para
                respuesta.pregunta = pregunta # asociarloo a la pregunta
                respuesta.evaluacion = evaluacion # asociarlo a la evaluacion
                respuesta.save() #  y ahora si lo guarda posta.
        return redirect('evaluaciones_empleado')
        
    context = {
            'empleado': empleado,
            'forms_comptencia':forms_competencia,          
        }
    
    template_name = 'indicadores/evaluacion_empleado.html'
    return render(request, template_name, context)