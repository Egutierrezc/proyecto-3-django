from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_salas, name='lista_salas'),
    path('sala/<int:sala_id>/', views.detalle_sala, name='detalle_sala'),
]