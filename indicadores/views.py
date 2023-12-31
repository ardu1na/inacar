from django.shortcuts import render, redirect
from indicadores.models import Evaluacion, RespuestaObjetivo, \
    Pregunta, RespuestaCompetencia, InformeAnual
from django.contrib.auth.decorators import login_required 
from indicadores.forms import RespuestaObjetivoEvaluadoForm, RespuestaObjetivoEvaluadorForm, \
    RespuestaCompetenciaEvaluadoForm, RespuestaCompetenciaEvaluadorForm
from datetime import date
from django.http import HttpResponse

today  = date.today()

@login_required
def ver_evaluacion_empleado(request, id):
    
    evaluacion = Evaluacion.objects.get(id=id)
    competencias = []
    subcompetencias = []
    respuestas_competencia = RespuestaCompetencia.objects.filter(evaluacion=evaluacion)
    
    for respuesta_competencia in respuestas_competencia:
        if respuesta_competencia.pregunta.competencia not in competencias:
            competencias.append(respuesta_competencia.pregunta.competencia)
        if respuesta_competencia.pregunta not in subcompetencias:
            subcompetencias.append(respuesta_competencia.pregunta)
    
    context = {
        'evaluacion': evaluacion,
        'competencias': competencias,
        'subcompetencias': subcompetencias,
    }

    return render(request, 'indicadores/ver_evaluacion.html', context)

        
       


############################# EVALUACIONES DE LOS EMPLEADOS
@login_required
def evaluaciones_empleado(request):
    empleado = request.user.empleado
    evaluaciones = Evaluacion.objects.filter(empleado=empleado)
    anio_actual = today.year
    try:
        informe_anual = InformeAnual.objects.get(empleado=empleado, periodo__year=anio_actual)
    
        context = {
            'empleado': empleado,
            'evaluaciones': evaluaciones,
            'informe_anual': informe_anual,
            'anio': anio_actual
            
        }
    except InformeAnual.DoesNotExist:
        context = {
            'empleado': empleado,
            'evaluaciones': evaluaciones,
            'anio': anio_actual

        }

    template_name = 'indicadores/empleado_evaluaciones.html'
    return render(request, template_name, context)







@login_required 
def nueva_evaluacion(request):
# si es operativo que  no muestre objetivos sino competencias
    empleado = request.user.empleado

    if request.method == "GET": # crear una nueva instancia al empezar
        evaluacion = Evaluacion.objects.create(empleado=empleado, lider=empleado.lider)
        try:
            informe_anual = InformeAnual.objects.get(empleado=empleado, lider=empleado.lider, periodo__year=today.year)
            
        except InformeAnual.DoesNotExist:
            informe_anual =  InformeAnual.objects.create(empleado=empleado, lider=empleado.lider, periodo=evaluacion.fecha)
        evaluacion.informe_anual=informe_anual
        evaluacion.save()
        informe_anual.save()
    objetivos = empleado.cargo.objetivos.all() 

    if objetivos:     ## si el empleado tiene objetivos asociados

        ## crear nueva evaluacion con formulario de objetivos

        ### formulario de objetivos para el cargo del empleado
        forms_objetivo = [] 
        for objetivo in objetivos:
            form_objetivo = RespuestaObjetivoEvaluadoForm(request.POST or None, prefix=f'objetivo_{objetivo.pk}')
            forms_objetivo.append((objetivo, form_objetivo))
            
        if 'objetivo' in request.POST:
            evaluacion_id = request.POST.get('evaluacion_id')
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)
            for objetivo, form_objetivo in forms_objetivo:
                form_objetivo = RespuestaObjetivoEvaluadoForm(request.POST, prefix=f'objetivo_{objetivo.pk}')
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
        preguntas = Pregunta.objects.filter(competencia__nivel_administrativo=empleado.nivel_administrativo)
        
        forms_competencia = []
        
        for pregunta in preguntas:
            form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
            forms_competencia.append((pregunta, form_competencia))
        
        if 'competencia' in request.POST:
            evaluacion_id = request.POST.get('evaluacion_id', None)
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)

            for pregunta, form_competencia in forms_competencia:
                form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST, prefix=f'pregunta_{pregunta.pk}')
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
    preguntas = Pregunta.objects.filter(competencia__nivel_administrativo=empleado.nivel_administrativo)
    forms_competencia = []
    for pregunta in preguntas:
        form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
        forms_competencia.append((pregunta, form_competencia))
    
    if 'competencia' in request.POST:
        for pregunta, form_competencia in forms_competencia:
            form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST, prefix=f'pregunta_{pregunta.pk}')
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



## que el lider responda su propio examen
## que vea los empleados


@login_required
def evaluaciones_lider(request):
    lider = request.user.lider
    evaluaciones = Evaluacion.objects.filter(lider=lider)
    context = {
        'lider': lider,
        'evaluaciones': evaluaciones,
    }

    template_name = 'indicadores/empleados_evaluaciones.html'
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
            form_objetivo = RespuestaObjetivoEvaluadorForm(instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
            forms_objetivo.append((respuestaobjetivo, form_objetivo))
    else: 
        return redirect('evaluacion_competencia_lider', id=evaluacion.id)

    if request.method == 'POST' and 'objetivo' in request.POST:
        evaluacion_id = request.POST.get('evaluacion_id')
        evaluacion = Evaluacion.objects.get(id=evaluacion_id)

        for respuestaobjetivo, form_objetivo in forms_objetivo:
            form_objetivo = RespuestaObjetivoEvaluadorForm(request.POST, instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
            if form_objetivo.is_valid():
                form_objetivo.save()

        return redirect('evaluacion_competencia_lider', id=evaluacion.id)
    
    context = {
                'lider': lider,
                'forms_objetivo': forms_objetivo,
                'evaluacion': evaluacion,          
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
        form_competencia = RespuestaCompetenciaEvaluadorForm(request.POST or None,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
        forms_competencia.append((pregunta, form_competencia))

    if request.method == 'POST' and 'competencia' in request.POST:
        evaluacion_id = request.POST.get('evaluacion_id')
        evaluacion = Evaluacion.objects.get(id=evaluacion_id)
        for pregunta, form_competencia in forms_competencia:
            form_competencia = RespuestaCompetenciaEvaluadorForm(request.POST,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
            if form_competencia.is_valid():
                form_competencia.save() 
        return redirect('evaluaciones_lider')
        
    context = {
            'lider': lider,
            'forms_comptencia':forms_competencia,
            'evaluacion': evaluacion,          
        }
    
    template_name = 'indicadores/evaluacion_lider.html'
    return render(request, template_name, context)





################################################################################ EVALUACIONES de los DIRECTORES




############################# EVALUACIONES A LOS LIDERES
@login_required # el lider ve las evaluacionoes de sii mismo 
def lider_evaluaciones(request):
    lider = request.user.lider
    evaluaciones = []
    evaluaciones_del_lider = Evaluacion.objects.filter(lider=lider)
    for evaluacion_lider in evaluaciones_del_lider:
        if evaluacion_lider.director:
            evaluaciones.append(evaluacion_lider)
    context = {
        'lider': lider,
        'evaluaciones': evaluaciones,
    }

    template_name = 'indicadores/lider_evaluaciones.html'
    return render(request, template_name, context)

@login_required # el lider empieza a autoevaluarse
def lider_nueva_evaluacion(request):
# si es operativo que  no muestre objetivos sino competencias
    lider = request.user.lider

    if request.method == "GET": # crear una nueva instancia al empezar 
        evaluacion = Evaluacion.objects.create(lider=lider, director=lider.director)
        
        try:
            informe_anual = InformeAnual.objects.get(lider=lider, director=lider.director, periodo__year=today.year)
        except InformeAnual.DoesNotExist:
            informe_anual =  InformeAnual.objects.create(lider=lider, director=lider.director, periodo=evaluacion.fecha)
        evaluacion.informe_anual=informe_anual
        evaluacion.save()   

    objetivos = lider.cargo.objetivos.all() 

    if objetivos:     ## si el empleado tiene objetivos asociados

        ## crear nueva evaluacion con formulario de objetivos

        ### formulario de objetivos para el cargo del empleado
        forms_objetivo = [] 
        for objetivo in objetivos:
            form_objetivo = RespuestaObjetivoEvaluadoForm(request.POST or None, prefix=f'objetivo_{objetivo.pk}')
            forms_objetivo.append((objetivo, form_objetivo))
            
        if 'objetivo' in request.POST:
            evaluacion_id = request.POST.get('evaluacion_id')
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)
            for objetivo, form_objetivo in forms_objetivo:
                form_objetivo = RespuestaObjetivoEvaluadoForm(request.POST, prefix=f'objetivo_{objetivo.pk}')
                if form_objetivo.is_valid():
                    respuesta = form_objetivo.save(commit=False) # que hace esto, lo preguarda para
                    respuesta.objetivo = objetivo # asociarloo al objetivo
                    respuesta.evaluacion = evaluacion # asociarlo a la evaluacion
                    respuesta.save() #  y ahora si lo guarda posta.
            return redirect('lider_evaluacion_competencia', id=evaluacion.id)
            
                
            """            
            AQUI hay que redirecionar al empleado al fomrulario de comptenencias que es otra vista
            
            """
        context = {
            'lider': lider,
            'forms_objetivo':forms_objetivo,      
            'evaluacion':evaluacion    
        }
    
    else:         
        ## si el lider NO TIENE objetivos asociados       
        
        ######## formularios de comptencias get
        preguntas = Pregunta.objects.filter(competencia__nivel_administrativo=lider.nivel_administrativo)
        
        forms_competencia = []
        
        for pregunta in preguntas:
            form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
            forms_competencia.append((pregunta, form_competencia))
        
        if 'competencia' in request.POST:
            evaluacion_id = request.POST.get('evaluacion_id', None)
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)

            for pregunta, form_competencia in forms_competencia:
                form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST, prefix=f'pregunta_{pregunta.pk}')
                if form_competencia.is_valid():
                    respuesta = form_competencia.save(commit=False) # que hace esto, lo preguarda para
                    respuesta.pregunta = pregunta # asociarloo a la pregunta
                    respuesta.evaluacion = evaluacion # asociarlo a la evaluacion
                    respuesta.save() #  y ahora si lo guarda posta.
            return redirect('lider_evaluaciones')
            
        context = {
                'lider': lider,
                'forms_comptencia':forms_competencia, 
                'evaluacion':evaluacion    
         
            }

    template_name = 'indicadores/lider_evaluacion.html'
    return render(request, template_name, context)

@login_required
def lider_evaluacion_competencia(request, id):
    
    lider = request.user.lider
    evaluacion = Evaluacion.objects.get(id=id)
    preguntas = Pregunta.objects.filter(competencia__nivel_administrativo=lider.nivel_administrativo)
    forms_competencia = []
    for pregunta in preguntas:
        form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
        forms_competencia.append((pregunta, form_competencia))
    
    if 'competencia' in request.POST:
        for pregunta, form_competencia in forms_competencia:
            form_competencia = RespuestaCompetenciaEvaluadoForm(request.POST, prefix=f'pregunta_{pregunta.pk}')
            if form_competencia.is_valid():
                respuesta = form_competencia.save(commit=False) # que hace esto, lo preguarda para
                respuesta.pregunta = pregunta # asociarloo a la pregunta
                respuesta.evaluacion = evaluacion # asociarlo a la evaluacion
                respuesta.save() #  y ahora si lo guarda posta.
        return redirect('lider_evaluaciones')
        
    context = {
            'lider': lider,
            'forms_comptencia':forms_competencia,          
        }
    
    template_name = 'indicadores/lider_evaluacion.html'
    return render(request, template_name, context)

############################# Respuestas DE LOS DIRECTORES

@login_required # el director ver las evaluaciones de los lideres
def director_evaluaciones(request):
    director = request.user.director
    evaluaciones = Evaluacion.objects.filter(director=director)
    context = {
        'director': director,
        'evaluaciones': evaluaciones,
    }

    template_name = 'indicadores/director_evaluaciones.html'
    return render(request, template_name, context)


@login_required 
def evaluar_lider(request, id):
    director = request.user.director
    
    evaluacion = Evaluacion.objects.get(id=id) 
    
    # ver si la evaluacion tiene objetivos
    respuestas_objetivo = RespuestaObjetivo.objects.filter(evaluacion=evaluacion)
    if respuestas_objetivo:
        
        forms_objetivo = []                   
        
        for respuestaobjetivo in respuestas_objetivo:
            form_objetivo = RespuestaObjetivoEvaluadorForm(instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
            forms_objetivo.append((respuestaobjetivo, form_objetivo))

        if request.method == 'POST':
            for respuestaobjetivo, form_objetivo in forms_objetivo:
                form_objetivo = RespuestaObjetivoEvaluadorForm(request.POST, instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
                if form_objetivo.is_valid():
                    form_objetivo.save()
            return redirect('evaluacion_competencia_director', id=evaluacion.id)
            
        context = {
                'director': director,
                'forms_comptencia': forms_objetivo,          
            }
    
    else:
        # si la evaluacion no tiene objetivos
        respuestas_competencia = RespuestaCompetencia.objects.filter(evaluacion=evaluacion)
        if respuestas_competencia:
            
        ######## formularios de comptencias get
            forms_competencia = []
        
            for pregunta in respuestas_competencia:
                form_competencia = RespuestaCompetenciaEvaluadorForm(request.POST or None,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
                forms_competencia.append((pregunta, form_competencia))
            
        if 'competencia' in request.POST:
            for pregunta, form_competencia in forms_competencia:
                form_competencia = RespuestaCompetenciaEvaluadorForm(request.POST,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
                if form_competencia.is_valid():
                    form_competencia.save()
                else:
                    return HttpResponse(f'{form_competencia.errors}')
 
            return redirect('director_evaluaciones')
            
        context = {
                'director': director,
                'forms_comptencia':forms_competencia,          
            }

    template_name = 'indicadores/evaluacion_director.html'
    return render(request, template_name, context)

@login_required
def evaluacion_competencia_director(request, id):
    
    director = request.user.director
    evaluacion = Evaluacion.objects.get(id=id)
    
    respuestas_competencia = RespuestaCompetencia.objects.filter(evaluacion=evaluacion)
        
    ######## formularios de comptencias get
    forms_competencia = []

    for pregunta in respuestas_competencia:
        form_competencia = RespuestaCompetenciaEvaluadorForm(request.POST or None,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
        forms_competencia.append((pregunta, form_competencia))
    
    if 'competencia' in request.POST:
        for pregunta, form_competencia in forms_competencia:
            form_competencia = RespuestaCompetenciaEvaluadorForm(request.POST,instance=pregunta, prefix=f'pregunta_{pregunta.pk}')
            if form_competencia.is_valid():
                form_competencia.save() 
            else:
                return HttpResponse(f'{form_competencia.errors}')

        return redirect('director_evaluaciones')
        
    context = {
            'director': director,
            'forms_comptencia':forms_competencia,          
        }
    
    template_name = 'indicadores/evaluacion_director.html'
    return render(request, template_name, context)
