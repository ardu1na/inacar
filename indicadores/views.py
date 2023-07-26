from django.shortcuts import render, redirect
from indicadores.models import Evaluacion, RespuestaObjetivo
from django.contrib.auth.decorators import login_required 
from indicadores.forms import RespuestaObjetivoEmpleadoForm, RespuestaObjetivoLiderForm
from django.http import HttpResponse



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
def evaluacion(request, id=None):
    
    # evaluacion para el empleado
    
        try:
        
            empleado = request.user.empleado
            
            ### si hay id quiere decir que es para ver una evaluacion ya hecha en el pasado
            if id: # para ver una evaluación ya realizada
                if request.method == 'GET':
                    
                    evaluacion = Evaluacion.objects.get(id=id)
                    respuestas_objetivo = RespuestaObjetivo.objects.filter(evaluacion=evaluacion)
                    print(respuestas_objetivo)
                        
                        
                context = {
                    'evaluacion': evaluacion,
                    
                }
                        
                print(f'se ha obtenido la instancia de evaluacion {evaluacion} id:{evaluacion.id}')
                    
                    
            else: # para empezar una nueva evaluación
                evaluacion = Evaluacion.objects.create(empleado=empleado, lider=empleado.lider)
                objetivos = empleado.cargo.objetivos.all()
                forms_objetivo = []
                for objetivo in objetivos:
                    form_objetivo = RespuestaObjetivoEmpleadoForm(request.POST or None, prefix=f'objetivo_{objetivo.pk}')
                    forms_objetivo.append((objetivo, form_objetivo))

                if request.method == 'POST':
                    evaluacion = Evaluacion.objects.filter(empleado=empleado).last()
                    for objetivo, form_objetivo in forms_objetivo:
                        form_objetivo = RespuestaObjetivoEmpleadoForm(request.POST, prefix=f'objetivo_{objetivo.pk}')
                        if form_objetivo.is_valid():
                            respuesta = form_objetivo.save(commit=False)
                            respuesta.objetivo = objetivo
                            respuesta.evaluacion = evaluacion
                            respuesta.save()

                    return redirect('success')

        

                context = {
                    'forms_objetivo': forms_objetivo,
                    'evaluacion': evaluacion,
                }

            template_name = 'indicadores/evaluacion.html'
            return render(request, template_name, context)
        except:
            # evaluacion para el lider
            if request.user.lider:
                
                lider = request.user.lider
                evaluacion = Evaluacion.objects.last() 
                # la evaluacion tiene que venir o de crear una nueva evaluacion por parte del lider y asignarla a sus empleados
                # o de buscarla y viene con su pk, id. 
                respuestas_objetivo = RespuestaObjetivo.objects.filter(evaluacion=evaluacion)
                
                forms_objetivo = []                   
                
                for respuestaobjetivo in respuestas_objetivo:
                    form_objetivo = RespuestaObjetivoLiderForm(instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
                    forms_objetivo.append((respuestaobjetivo, form_objetivo))

                if request.method == 'POST':

                    for respuestaobjetivo, form_objetivo in forms_objetivo:
                        form_objetivo = RespuestaObjetivoLiderForm(request.POST, instance=respuestaobjetivo, prefix=f'respuestaobjetivo_{respuestaobjetivo.pk}')
                        if form_objetivo.is_valid():
                            form_objetivo.save()

                    return redirect('success')
                print(respuestas_objetivo)
                context = {
                    'lider': lider,
                    'evaluacion': evaluacion,
                    'respuestas_objetivo': respuestas_objetivo,
                    'forms_objetivo': forms_objetivo
                }

                template_name = 'indicadores/evaluacion.html'
                return render(request, template_name, context)
            else:
                return HttpResponse('El usuario actual no está asociado ni a un empleado ni a un lider')
    
def success(request):
    return HttpResponse("formualrio enviado!")
