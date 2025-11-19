from django.contrib import admin
from .models import Sala, Reserva

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 
        'capacidad_maxima', 
        'habilitada',
        'esta_reservada' 
    )
    list_filter = ('habilitada', 'esta_reservada')
    search_fields = ('nombre',)
    list_editable = ('habilitada',) 


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'sala', 
        'rut_persona', 
        'fecha_hora_inicio', 
        'fecha_hora_termino'
    )
    list_filter = ('sala',)
    search_fields = ('rut_persona',)
    fields = (
        'sala', 
        'rut_persona', 
        'fecha_hora_inicio', 
        'fecha_hora_termino'
    )