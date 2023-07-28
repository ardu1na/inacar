from django.shortcuts import render, redirect
from indicadores.models import Evaluacion, RespuestaObjetivo, \
    Competencia, Pregunta, RespuestaCompetencia
from django.contrib.auth.decorators import login_required 
from indicadores.forms import RespuestaObjetivoEmpleadoForm, RespuestaObjetivoLiderForm, \
    RespuestaCompetenciaEmpleadoForm, RespuestaCompetenciaLiderForm
from django.http import HttpResponse
from django.urls import reverse


############################# EVALUACIONES DE LOS EMPLEADOS
@login_required
def evaluaciones_empleado(request):
    empleado = request.user.empleado
    evaluaciones = Evaluacion.objects.filter(empleado=empleado)
    context = {
        'empleado': empleado,
        'evaluaciones': evaluaciones,
    }

    template_name = 'indicadores/evaluaciones.html'
    return render(request, template_name, context)


@login_required 
def nueva_evaluacion(request):
# si es operativo que  no muestre objetivos sino competencias
    empleado = request.user.empleado

    if request.method == "GET":
        evaluacion = Evaluacion.objects.create(empleado=empleado, lider=empleado.lider)


    objetivos = empleado.cargo.objetivos.all() 

    if objetivos:     ## si el empleado tiene objetivos asociados

        ## crear nueva evaluacion con formulario de objetivos

        ### formulario de objetivos para el cargo del empleado
        forms_objetivo = [] 
        for objetivo in objetivos:
            form_objetivo = RespuestaObjetivoEmpleadoForm(request.POST or None, prefix=f'objetivo_{objetivo.pk}')
            forms_objetivo.append((objetivo, form_objetivo))
            
        if 'objetivo' in request.POST:
            evaluacion_id = request.POST.get('evaluacion_id')
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)
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
            'evaluacion':evaluacion    
        }
    
    else:         
        ## si el empleado NO TIENE objetivos asociados       
        
        ######## formularios de comptencias get
        preguntas = Pregunta.objects.all()
        forms_competencia = []
        for pregunta in preguntas:
            form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
            forms_competencia.append((pregunta, form_competencia))
        
        if 'competencia' in request.POST:
            evaluacion_id = request.POST.get('evaluacion_id', None)
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)

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
                'evaluacion':evaluacion    
         
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




############################# EVALUACIONES DE LOS LIDERES
@login_required
def evaluaciones_lider(request):
    lider = request.user.lider
    evaluaciones = Evaluacion.objects.filter(lider=lider)
    context = {
        'lider': lider,
        'evaluaciones': evaluaciones,
    }

    template_name = 'indicadores/evaluaciones.html'
    return render(request, template_name, context)





@login_required 
def responder_evaluacion(request, id):
    lider = request.user.lider
    
    evaluacion = Evaluacion.objects.get(id=id) 
    
    # ver si la evaluacion tiene objetivos
    respuestas_objetivo = RespuestaObjetivo.objects.filter(evaluacion=evaluacion)
    if respuestas_objetivo:
        
        forms_objetivo = []                   
        
        for respuestaobjetivo in respuestas_objetivo:
            form_objetivo = RespuestaObjetivoLiderForm(instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
            forms_objetivo.append((respuestaobjetivo, form_objetivo))

        if request.method == 'POST' and 'objetivo' in request.POST:

            for respuestaobjetivo, form_objetivo in forms_objetivo:
                form_objetivo = RespuestaObjetivoLiderForm(request.POST, instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
                if form_objetivo.is_valid():
                    form_objetivo.save()

            return redirect('evaluacion_competencia_lider', id=evaluacion.id)
    
        context = {
                'lider': lider,
                'forms_comptencia': forms_objetivo,          
            }
    
    else:
        # si la evaluacion no tiene objetivos
        respuestas_competencia = RespuestaCompetencia.objects.filter(evaluacion=evaluacion)
        if respuestas_competencia:
            
        ######## formularios de comptencias get
            forms_competencia = []
        
            for pregunta in respuestas_competencia:
                form_competencia = RespuestaCompetenciaLiderForm(request.POST or None,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
                forms_competencia.append((pregunta, form_competencia))
            
        if 'competencia' in request.POST:
            for pregunta, form_competencia in forms_competencia:
                form_competencia = RespuestaCompetenciaLiderForm(request.POST,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
                if form_competencia.is_valid():
                    form_competencia.save() 
            return redirect('evaluaciones_lider')
            
        context = {
                'lider': lider,
                'forms_comptencia':forms_competencia,          
            }

    template_name = 'indicadores/evaluacion_lider.html'
    return render(request, template_name, context)



@login_required
def evaluacion_competencia_lider(request, id):
    
    lider = request.user.lider
    evaluacion = Evaluacion.objects.get(id=id)
    
    respuestas_competencia = RespuestaCompetencia.objects.filter(evaluacion=evaluacion)
        
    ######## formularios de comptencias get
    forms_competencia = []

    for pregunta in respuestas_competencia:
        form_competencia = RespuestaCompetenciaLiderForm(request.POST or None,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
        forms_competencia.append((pregunta, form_competencia))
    
    if 'competencia' in request.POST:
        for pregunta, form_competencia in forms_competencia:
            form_competencia = RespuestaCompetenciaLiderForm(request.POST,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
            if form_competencia.is_valid():
                form_competencia.save() 
        return redirect('evaluaciones_lider')
        
    context = {
            'lider': lider,
            'forms_comptencia':forms_competencia,          
        }
    
    template_name = 'indicadores/evaluacion_lider.html'
    return render(request, template_name, context)