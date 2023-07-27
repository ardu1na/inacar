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
    try:
        if request.user.empleado:
            empleado = request.user.empleado
            evaluaciones = Evaluacion.objects.filter(empleado=empleado)
            context = {
                'empleado': empleado,
                'evaluaciones': evaluaciones,
            }

            template_name = 'indicadores/evaluaciones_empleado.html'
            return render(request, template_name, context)
            
    except:
        return HttpResponse("no eres empleado")

@login_required
def evaluacion_empleado(request, id=None):
    
        
    empleado = request.user.empleado
    
    ### si hay id quiere decir que es para ver una evaluacion ya hecha en el pasado
    if id: # para ver una evaluación ya realizada
                    
        evaluacion = Evaluacion.objects.get(id=id)
        forms_competencia = []                   


        if "changed" in request.GET: ###############################################################################################################33
            preguntas = Pregunta.objects.all()
            for pregunta in preguntas:
                form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
                forms_competencia.append((pregunta, form_competencia))
            

        if request.method == 'POST' and 'competencia' in request.POST:
            for competencia, form_competencia in forms_competencia:
                form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST, prefix=f'competencia_{competencia.pk}')
                if form_competencia.is_valid():
                    respuesta = form_competencia.save(commit=False)
                    
                    respuesta.pregunta = competencia
                    respuesta.evaluacion = evaluacion
                    respuesta.save()
                    
            return redirect('evaluaciones_empleado')
    
                            
        context = {
            'evaluacion': evaluacion,
            'forms_competencia': forms_competencia,
        }
                
            
            
            
            
            
    else: # si no tiene id EMpezar una nueva evaluación
        evaluacion = Evaluacion.objects.create(empleado=empleado, lider=empleado.lider)
        
        ######## formularios de objetivos get
        objetivos = empleado.cargo.objetivos.all()
        forms_objetivo = []
        for objetivo in objetivos:
            form_objetivo = RespuestaObjetivoEmpleadoForm(request.POST or None, prefix=f'objetivo_{objetivo.pk}')
            forms_objetivo.append((objetivo, form_objetivo))
            
        ######## formularios de comptencias get
        preguntas = Pregunta.objects.all()
        forms_competencia = []
        for pregunta in preguntas:
            form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST or None, prefix=f'pregunta_{pregunta.pk}')
            forms_competencia.append((pregunta, form_competencia))
        
        ### POST GRAL
        if request.method == 'POST':
            # se obtiene la evaluacion particular
            evaluacion = evaluacion
            
            
            ####### formulario de objetivos post
            if 'objetivo' in request.POST:
                print('objetivo')
                for objetivo, form_objetivo in forms_objetivo:
                    form_objetivo = RespuestaObjetivoEmpleadoForm(request.POST, prefix=f'objetivo_{objetivo.pk}')
                    if form_objetivo.is_valid():
                        respuesta = form_objetivo.save(commit=False)
                        respuesta.objetivo = objetivo
                        respuesta.evaluacion = evaluacion
                        respuesta.save()
                return redirect(reverse('evaluacion_empleado', args=[evaluacion.id]) + "?changed")

            ####### formulario de COMPETENCIAS POST
            ### todos tienen las mismas competencias excpeto "gestion humana"
            ## si es gestion_humana tiene una competencia
            ## gestion_humana es un cargo
            if 'competencia' in request.POST:
                print('competencia')
                for competencia, form_competencia in forms_competencia:
                    form_competencia = RespuestaCompetenciaEmpleadoForm(request.POST, prefix=f'competencia_{competencia.pk}')
                    if form_competencia.is_valid():
                        respuesta = form_competencia.save(commit=False)
                        
                        respuesta.pregunta = competencia
                        respuesta.evaluacion = evaluacion
                        respuesta.save()
                        
                return redirect('evaluaciones_empleado')

        context = {
            'forms_objetivo': forms_objetivo,
            'evaluacion': evaluacion,
            'forms_competencia': forms_competencia
        }






    template_name = 'indicadores/evaluacion_empleado.html'
    return render(request, template_name, context)

        
        
        
        
    
def success(request):
    return HttpResponse("formualrio enviado!")
