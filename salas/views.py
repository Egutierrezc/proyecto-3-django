from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Sala, Reserva
from .forms import ReservaForm

def actualizar_disponibilidad():
    now = timezone.now()
    
    reservas_expiradas = Reserva.objects.filter(
        fecha_hora_termino__lte=now,
        sala__esta_reservada=True
    ).select_related('sala')
    
    salas_a_liberar_ids = list(set([reserva.sala.id for reserva in reservas_expiradas]))
    
    if salas_a_liberar_ids:
        Sala.objects.filter(
            id__in=salas_a_liberar_ids
        ).update(esta_reservada=False)


def lista_salas(request):
    actualizar_disponibilidad()
    
    salas = Sala.objects.filter(habilitada=True).order_by('nombre')
    
    context = {
        'salas': salas,
        'titulo': "Salas de Estudio ITID"
    }
    return render(request, 'salas/lista_salas.html', context)


def detalle_sala(request, sala_id):
    actualizar_disponibilidad()
    
    sala = get_object_or_404(Sala, pk=sala_id)
    reserva_actual = None
    form = None
    
    if sala.esta_reservada:
        reserva_actual = Reserva.objects.filter(
            sala=sala, 
            fecha_hora_termino__gt=timezone.now()
        ).order_by('-fecha_hora_inicio').first()
        
    elif request.method == 'POST' and sala.habilitada:
        form = ReservaForm(request.POST)
        
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.sala = sala
            reserva.save()
            
            sala.esta_reservada = True
            sala.save()
            
            return redirect('lista_salas')
            
    else:
        form = ReservaForm()
    
    context = {
        'sala': sala,
        'reserva_actual': reserva_actual,
        'form': form
    }
    return render(request, 'salas/detalle_sala.html', context)