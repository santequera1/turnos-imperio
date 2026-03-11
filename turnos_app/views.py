from .models import Turno, ClienteFrecuente
from .forms import TurnoForm, ReiniciarNumerosForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime
import os
import csv
import json
from io import StringIO


@login_required
def agendar_turno(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id', None)
        placa = request.POST.get('placa', '').strip()
        form = TurnoForm(request.POST)

        if form.is_valid():
            turno = form.save(commit=False)

            if cliente_id:
                cliente_frecuente = get_object_or_404(ClienteFrecuente, id=cliente_id)
                turno.cliente_frecuente = cliente_frecuente
                if placa:
                    cliente_frecuente.placa = placa
                    cliente_frecuente.save()
            else:
                cliente_frecuente, created = ClienteFrecuente.objects.get_or_create(
                    numero_telefono=turno.numero_telefono,
                    defaults={
                        'nombre_cliente': turno.nombre_cliente,
                        'referencia_motocicleta': turno.referencia_motocicleta,
                        'placa': placa,
                    }
                )
                if not created and placa:
                    cliente_frecuente.placa = placa
                    cliente_frecuente.save()
                turno.cliente_frecuente = cliente_frecuente

            turno.save()

    else:
        form = TurnoForm()

    context = {'form': form}
    return render(request, 'turnos_app/agendar_turno.html', context)


def buscar_clientes(request):
    q = request.GET.get('q', '')
    clientes = ClienteFrecuente.objects.filter(
        Q(nombre_cliente__icontains=q) |
        Q(referencia_motocicleta__icontains=q) |
        Q(placa__icontains=q) |
        Q(numero_telefono__icontains=q)
    )[:10]
    data = [
        {
            'id': c.id,
            'nombre_cliente': c.nombre_cliente,
            'numero_telefono': c.numero_telefono,
            'referencia_motocicleta': c.referencia_motocicleta,
            'placa': c.placa or '',
        } for c in clientes
    ]
    return JsonResponse(data, safe=False)



def pagina_principal(request):
    return render(request, 'turnos_app/pagina_principal.html')


def lista_turnos(request):
    turnos = Turno.objects.filter(finalizado=False).order_by('orden', 'id')
    context = {'turnos': turnos}
    return render(request, 'turnos_app/lista_turnos.html', context)


@require_GET
def api_turnos_ordenados(request):
    turnos = Turno.objects.filter(finalizado=False).order_by('orden', 'id')
    data = [
        {
            "id": t.id,
            "numero_turno": t.numero_turno,
            "nombre_cliente": t.nombre_cliente,
            "referencia_motocicleta": t.referencia_motocicleta or "",
        }
        for t in turnos
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def atender_turnos(request):
    turnos = Turno.objects.filter(finalizado=False).order_by('orden', 'id').select_related()

    if request.method == 'POST':
        turno_id = request.POST.get('atender')
        if turno_id:
            turno_atendido = Turno.objects.get(id=turno_id)
            turno_atendido.finalizado = True
            turno_atendido.en_reparacion = False
            turno_atendido.fecha_finalizacion = timezone.now()
            turno_atendido.save()
        return redirect('atender_turnos')

    context = {'turnos': turnos}
    return render(request, 'turnos_app/atender_turnos.html', context)


@csrf_exempt
def actualizar_orden_turnos(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for item in data['order']:
                turno = Turno.objects.get(id=item['id'])
                turno.orden = item['position']
                turno.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def reiniciar_numeros(request):
    if request.method == 'POST':
        form = ReiniciarNumerosForm(request.POST)
        if form.is_valid() and form.cleaned_data['reiniciar']:
            nuevos_numeros = 1
            for turno in Turno.objects.filter(finalizado=False):
                turno.numero_turno = nuevos_numeros
                turno.save()
                nuevos_numeros += 1

            return redirect('lista_turnos')

    else:
        form = ReiniciarNumerosForm()

    context = {'form': form}
    return render(request, 'turnos_app/reiniciar_numeros.html', context)


@csrf_exempt
def descargar_csv(request):
    ahora = datetime.now().strftime('%d/%m/%Y -%H:%M:%S')
    clientes_atendidos = Turno.objects.filter(finalizado=False)

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(["Nombre Cliente", "Referencia Motocicleta", "Numero de Teléfono", "Reparacion", "Fecha"])

    for cliente in clientes_atendidos:
        csv_writer.writerow([cliente.nombre_cliente, cliente.referencia_motocicleta, cliente.numero_telefono, cliente.motivo_reparacion, ahora])

    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="datos_clientes.csv"'

    return response


def imprimir_datos(request):
    ahora = datetime.now().strftime('%d/%m/%Y -%H:%M:%S')
    clientes_atendidos = Turno.objects.filter(finalizado=False)
    buffer = StringIO()
    writer = csv.writer(buffer)

    if os.path.exists('datos_clientes.csv') and os.path.getsize('datos_clientes.csv') > 0:
        with open('datos_clientes.csv', 'r') as csvfile:
            existing_data = csv.reader(csvfile)
            for row in existing_data:
                writer.writerow(row)

    for cliente in clientes_atendidos:
        writer.writerow([cliente.nombre_cliente,
        cliente.referencia_motocicleta,
        cliente.numero_telefono, cliente.motivo_reparacion,
        ahora])

    with open('datos_clientes.csv', 'w', encoding='utf-8', newline='') as csvfile:
        csvfile.write(buffer.getvalue())

    csv_data = []
    with open("datos_clientes.csv", "r", encoding='utf-8', newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    context = {
        'clientes_atendidos': clientes_atendidos,
        'csv_data': csv_data,
    }
    return render(request, 'turnos_app/imprimir_datos.html', context)


def enviar_correo_atencion(request):
    if request.method == 'POST':
        ahora = datetime.now().strftime('%d/%m/%Y -%H:%M:%S')
        subject = 'Informe de turnos'
        message = 'Turnos del día: ' + ahora
        template = render_to_string('turnos_app/email_template.html', {
            'email': 'santequera@wailus.co',
            'subject': subject,
            'message': message
        })

        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['santequera@wailus.co'],
        )

        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'datos_clientes.csv')
        if os.path.exists(csv_file_path):
            email.attach_file(csv_file_path, 'text/csv')

        email.fail_silently = False
        email.send()

        return redirect('lista_turnos')

    return HttpResponse('Método no permitido', status=405)


def obtener_lista_turnos(request):
    turnos = Turno.objects.filter(finalizado=False).values('nombre_cliente', 'referencia_motocicleta', 'numero_telefono', 'motivo_reparacion')
    lista_turnos = list(turnos)
    return JsonResponse({'turnos': lista_turnos})


@csrf_exempt
def actualizar_estado(request, turnoId):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            en_reparacion = data['en_reparacion']

            turno = Turno.objects.get(id=turnoId)
            turno.en_reparacion = en_reparacion == '1' or en_reparacion == True
            turno.save()

            return JsonResponse({
                'status': 'success',
                'en_reparacion': turno.en_reparacion
            })
        except Turno.DoesNotExist:
            return JsonResponse({'error': 'Turno no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def reiniciar_numeros_de_turno(request):
    Turno.objects.filter(finalizado=False).delete()

    csv_file_path = 'datos_clientes.csv'
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows([])

    return redirect('lista_turnos')


def buscar_cliente(request):
    term = request.GET.get('term')
    clientes = Turno.objects.filter(nombre_cliente__icontains=term, finalizado=False)[:5]
    results = [
        {
            'value': cliente.id,
            'label': f'{cliente.nombre_cliente} - {cliente.numero_telefono} - {cliente.referencia_motocicleta}',
            'nombre': cliente.nombre_cliente,
            'numero_telefono': cliente.numero_telefono,
            'referencia_motocicleta': cliente.referencia_motocicleta,
            'motivo_reparacion': cliente.motivo_reparacion,
        }
        for cliente in clientes
    ]
    return JsonResponse(results, safe=False)


# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    turnos = Turno.objects.filter(finalizado=True).order_by('-fecha_finalizacion')

    q = request.GET.get('q', '')
    if q:
        turnos = turnos.filter(
            Q(nombre_cliente__icontains=q) |
            Q(referencia_motocicleta__icontains=q)
        )

    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    if fecha_desde:
        turnos = turnos.filter(fecha_finalizacion__date__gte=fecha_desde)
    if fecha_hasta:
        turnos = turnos.filter(fecha_finalizacion__date__lte=fecha_hasta)

    paginator = Paginator(turnos, 20)
    page = request.GET.get('page')
    turnos_page = paginator.get_page(page)

    hoy = timezone.now().date()
    context = {
        'turnos': turnos_page,
        'total_clientes': ClienteFrecuente.objects.count(),
        'turnos_hoy': Turno.objects.filter(fecha_creacion__date=hoy).count(),
        'total_turnos': Turno.objects.filter(finalizado=True).count(),
        'turnos_activos': Turno.objects.filter(finalizado=False).count(),
        'q': q,
        'fecha_desde': fecha_desde or '',
        'fecha_hasta': fecha_hasta or '',
    }
    return render(request, 'turnos_app/dashboard.html', context)


@login_required
def dashboard_clientes(request):
    clientes = ClienteFrecuente.objects.annotate(
        visitas=Count('turno', filter=Q(turno__finalizado=True))
    ).order_by('-visitas')

    q = request.GET.get('q', '')
    if q:
        clientes = clientes.filter(
            Q(nombre_cliente__icontains=q) |
            Q(placa__icontains=q) |
            Q(numero_telefono__icontains=q) |
            Q(referencia_motocicleta__icontains=q)
        )

    paginator = Paginator(clientes, 20)
    page = request.GET.get('page')
    clientes_page = paginator.get_page(page)

    context = {
        'clientes': clientes_page,
        'q': q,
    }
    return render(request, 'turnos_app/dashboard_clientes.html', context)


@login_required
def dashboard_cliente_detalle(request, cliente_id):
    cliente = get_object_or_404(
        ClienteFrecuente.objects.annotate(
            visitas=Count('turno', filter=Q(turno__finalizado=True))
        ),
        id=cliente_id
    )
    turnos = Turno.objects.filter(cliente_frecuente=cliente).order_by('-fecha_creacion')

    context = {
        'cliente': cliente,
        'turnos': turnos,
    }
    return render(request, 'turnos_app/dashboard_cliente_detalle.html', context)


@login_required
def dashboard_cliente_editar(request, cliente_id):
    cliente = get_object_or_404(ClienteFrecuente, id=cliente_id)

    if request.method == 'POST':
        cliente.nombre_cliente = request.POST.get('nombre_cliente', cliente.nombre_cliente)
        cliente.numero_telefono = request.POST.get('numero_telefono', cliente.numero_telefono)
        cliente.referencia_motocicleta = request.POST.get('referencia_motocicleta', cliente.referencia_motocicleta)
        cliente.placa = request.POST.get('placa', cliente.placa)
        cliente.save()
        return redirect('dashboard_cliente_detalle', cliente_id=cliente.id)

    context = {'cliente': cliente}
    return render(request, 'turnos_app/dashboard_cliente_editar.html', context)


@login_required
def dashboard_cliente_eliminar(request, cliente_id):
    cliente = get_object_or_404(ClienteFrecuente, id=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('dashboard_clientes')

    context = {'cliente': cliente}
    return render(request, 'turnos_app/dashboard_cliente_eliminar.html', context)


@login_required
def api_buscar_clientes_dashboard(request):
    q = request.GET.get('q', '')
    moto = request.GET.get('moto', '')
    clientes = ClienteFrecuente.objects.annotate(
        visitas=Count('turno', filter=Q(turno__finalizado=True))
    ).order_by('-visitas')

    if q:
        clientes = clientes.filter(
            Q(nombre_cliente__icontains=q) |
            Q(placa__icontains=q) |
            Q(numero_telefono__icontains=q) |
            Q(referencia_motocicleta__icontains=q)
        )

    if moto:
        # Todas las palabras deben estar presentes (AND)
        for palabra in moto.split():
            clientes = clientes.filter(referencia_motocicleta__icontains=palabra)

    clientes = clientes[:30]
    data = [
        {
            'id': c.id,
            'nombre_cliente': c.nombre_cliente,
            'numero_telefono': c.numero_telefono,
            'referencia_motocicleta': c.referencia_motocicleta,
            'placa': c.placa or '-',
            'visitas': c.visitas,
        } for c in clientes
    ]
    return JsonResponse(data, safe=False)
