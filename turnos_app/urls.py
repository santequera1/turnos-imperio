from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('login/', LoginView.as_view(template_name='turnos_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
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
    path('buscar_clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('actualizar-estado/<int:turnoId>/', views.actualizar_estado, name='actualizar_estado'),
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('actualizar-orden-turnos/', views.actualizar_orden_turnos, name='actualizar_orden_turnos'),
    path('api/turnos-ordenados/', views.api_turnos_ordenados, name='api_turnos_ordenados'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/clientes/', views.dashboard_clientes, name='dashboard_clientes'),
    path('dashboard/clientes/<int:cliente_id>/', views.dashboard_cliente_detalle, name='dashboard_cliente_detalle'),
    path('dashboard/clientes/<int:cliente_id>/editar/', views.dashboard_cliente_editar, name='dashboard_cliente_editar'),
    path('dashboard/clientes/<int:cliente_id>/eliminar/', views.dashboard_cliente_eliminar, name='dashboard_cliente_eliminar'),
    path('api/buscar-clientes-dashboard/', views.api_buscar_clientes_dashboard, name='api_buscar_clientes_dashboard'),
]
