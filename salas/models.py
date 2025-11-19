from django.db import models
from django.utils import timezone
from datetime import timedelta

class Sala(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    
    capacidad_maxima = models.IntegerField(
        verbose_name="Capacidad Máxima"
    )
    
    esta_reservada = models.BooleanField(
        default=False,
        verbose_name="Reservada"
    )
    
    habilitada = models.BooleanField(
        default=True,
        verbose_name="Habilitada"
    )

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Sala de Estudio"
        verbose_name_plural = "Salas de Estudio"


class Reserva(models.Model):
    sala = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name="Sala Reservada"
    )
    
    rut_persona = models.CharField(
        max_length=12, 
        verbose_name="RUT de la Persona"
    )
    
    fecha_hora_inicio = models.DateTimeField(
        default=timezone.now,
        verbose_name="Inicio"
    )
    
    fecha_hora_termino = models.DateTimeField(
        verbose_name="Término"
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.fecha_hora_termino = self.fecha_hora_inicio + timedelta(hours=2)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.sala.nombre} por {self.rut_persona}"

    class Meta:
        verbose_name = "Reserva de Sala"
        verbose_name_plural = "Reservas de Salas"
        ordering = ['-fecha_hora_inicio']