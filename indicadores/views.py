from django.shortcuts import render, redirect
from indicadores.models import Evaluacion, RespuestaObjetivo
from django.contrib.auth.decorators import login_required 
from indicadores.forms import RespuestaObjetivoEmpleadoForm
from django.http import HttpResponse


@login_required
def evaluacion_empleado(request):
    if request.user.empleado is not None:
        
        empleado = request.user.empleado
        if request.method == 'GET':
            evaluacion = Evaluacion.objects.create(empleado=empleado)

        objetivos = empleado.cargo.objetivos.all()
        forms = []
        for objetivo in objetivos:
            form = RespuestaObjetivoEmpleadoForm(request.POST or None, prefix=f'objetivo_{objetivo.pk}')
            forms.append((objetivo, form))

        if request.method == 'POST':
            evaluacion = Evaluacion.objects.filter(empleado=empleado).last()
            for objetivo, form in forms:
                form = RespuestaObjetivoEmpleadoForm(request.POST, prefix=f'objetivo_{objetivo.pk}')
                if form.is_valid():
                    respuesta = form.save(commit=False)
                    respuesta.objetivo = objetivo
                    respuesta.evaluacion = evaluacion
                    respuesta.save()

            return redirect('success')

        context = {
            'forms': forms,
            'evaluacion': evaluacion,
        }

        template_name = 'indicadores/evaluacion.html'
        return render(request, template_name, context)
    else:
        return HttpResponse('El usuario actual no es un empleado a evaluar')
    
def success(request):
    return HttpResponse("formualrio enviado!")
