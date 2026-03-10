from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('agendar-turno/', views.agendar_turno, name='agendar_turno'),
    path('lista-turnos/', views.lista_turnos, name='lista_turnos'),
    path('atender-turnos/', views.atender_turnos, name='atender_turnos'),
    path('atender-turnos2/', views.atender_turnos, name='atender_turnos2'),
    path('reiniciar-numeros/', views.reiniciar_numeros, name='reiniciar_numeros'),
    path('borrar-registros/', views.reiniciar_numeros_de_turno, name='borrar-registros'),
    path('imprimir-datos/', views.imprimir_datos, name='imprimir_datos'),
    path('descargar-csv/', views.descargar_csv, name='descargar_csv'),
    path('enviar-correo-atencion/', views.enviar_correo_atencion, name='enviar_correo_atencion'),
    path('confirmar-reinicio/', views.enviar_correo_atencion, name='confirmar-reinicio'),
    path('obtener-lista-turnos/', views.obtener_lista_turnos, name='obtener_lista_turnos'),
    path('agendar-turno/llamar-cliente/<int:turno_id>/', views.llamar_cliente, name='llamar_cliente'),

]


