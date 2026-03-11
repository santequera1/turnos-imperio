from .forms import TurnoForm
from .models import Turno 
from django.shortcuts import render, redirect
from .forms import ReiniciarNumerosForm
import os
import csv
from io import StringIO
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from django.shortcuts import render, get_object_or_404




hoy = datetime.now()
ahora = hoy.strftime('%d/%m/%Y -%H:%M:%S')
fecha = str(ahora)


def agendar_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        
        if form.is_valid():
            numero_telefono = form.cleaned_data['numero_telefono']
            nombre = form.cleaned_data['nombre_cliente']
            motocicleta = form.cleaned_data['referencia_motocicleta']
            motivo = form.cleaned_data['motivo_reparacion']
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            

            form.save()
            


            # Leer los datos existentes del archivo CSV, si existe
            csv_data = []
            if os.path.exists("datos_clientes.csv"):
                with open("datos_clientes.csv", "r", encoding='utf-8', newline="") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    csv_data = list(csv_reader)

            # Si el archivo CSV está vacío, agrega los encabezados
            if not csv_data:
                csv_data.append(["Nombre cliente", "Ref Motocicleta", "Numero telefono", "Motivo", "Fecha"])

            # Agregar el nuevo cliente a la lista de datos
            nuevo_cliente = [nombre, motocicleta, numero_telefono, motivo, fecha]
            csv_data.append(nuevo_cliente)

            # Escribir la lista completa de clientes en el archivo CSV
            with open("datos_clientes.csv", "w", encoding='utf-8', newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(csv_data)
            
            os.system("cls")
            print("Nuevo turno agendado")
            print(numero_telefono + " | " + nombre + " | " + motocicleta + " | " + motivo + " | " + fecha)
            
            
    else:
        form = TurnoForm()

    #Quedarse en la misma página
    context = {'form': form}
    return render(request, 'turnos_app/agendar_turno.html', context)



def pagina_principal(request):
    return render(request, 'turnos_app/pagina_principal.html')

    
def lista_turnos(request):
    turnos = Turno.objects.all().order_by('id')
    medio = len(turnos) // 2
    primera_parte = turnos[:medio]
    segunda_parte = turnos[medio:]
    
    context = {'primera_parte': primera_parte, 'segunda_parte': segunda_parte}
    return render(request, 'turnos_app/lista_turnos.html', context)



@csrf_exempt
def atender_turnos(request):
    turnos = Turno.objects.all().order_by('id')
    if request.method == 'POST':
        turno_id = request.POST.get('atender')  # Obtener el ID del turno a atender
        if turno_id:
            turno_atendido = Turno.objects.get(id=turno_id)
            print(turno_id)
            turno_atendido.delete()
            
        

            
            # Agregar lógica para notificar al cliente sobre el turno atendido
        return redirect('atender_turnos')  # Redirigir de nuevo a la página de atender turnos
    context = {'turnos': turnos}  # Agregar el formulario al contexto
    return render(request, 'turnos_app/atender_turnos.html', context)






def reiniciar_numeros(request):
    if request.method == 'POST':
        form = ReiniciarNumerosForm(request.POST)
        if form.is_valid() and form.cleaned_data['reiniciar']:
            # Reiniciar los números de turno aquí
            nuevos_numeros = 1
            for turno in Turno.objects.all():
                turno.numero_turno = nuevos_numeros
                turno.save()
                nuevos_numeros += 1

            return redirect('lista_turnos')  # Redirigir a la lista de turnos después de reiniciar

    else:
        form = ReiniciarNumerosForm()

    context = {'form': form}
    return render(request, 'turnos_app/reiniciar_numeros.html', context)





@csrf_exempt
def descargar_csv(request):
    # Obtener los datos de los clientes que se atendieron durante el día
    clientes_atendidos = Turno.objects.all()

    # Crear un archivo CSV en memoria
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(["Nombre Cliente", "Referencia Motocicleta", "Numero de Teléfono","Reparacion", "Fecha"])

    for cliente in clientes_atendidos:
        csv_writer.writerow([cliente.nombre_cliente, cliente.referencia_motocicleta, cliente.numero_telefono,cliente.motivo_reparacion,str(ahora)])

    # Crear una respuesta HTTP con el archivo CSV
    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="datos_clientes.csv"'
    
    return response

def imprimir_datos(request):
    # Obtener los datos de los clientes que se atendieron durante el día
    clientes_atendidos = Turno.objects.all()
    # Crear un archivo CSV en memoria
    buffer = StringIO()
    writer = csv.writer(buffer)
    
    # Verificar si el archivo CSV ya contiene datos
    if os.path.exists('datos_clientes.csv') and os.path.getsize('datos_clientes.csv') > 0:
        # Si el archivo existe y tiene contenido, abrirlo en modo de lectura ('r')
        with open('datos_clientes.csv', 'r') as csvfile:
            # Leer los datos existentes del archivo y copiarlos al archivo en memoria
            existing_data = csv.reader(csvfile)
            for row in existing_data:
                writer.writerow(row)

    # Agregar los nuevos datos al archivo CSV en memoria
    for cliente in clientes_atendidos:
        writer.writerow([cliente.nombre_cliente, 
        cliente.referencia_motocicleta, 
        cliente.numero_telefono,cliente.motivo_reparacion, 
        str(ahora)])
    
    # Guardar los datos en el archivo CSV en el sistema de archivos
    with open('datos_clientes.csv', 'w', encoding='utf-8', newline='') as csvfile:
        csvfile.write(buffer.getvalue())

    # Leer el contenido del archivo CSV
    csv_data = []
    with open("datos_clientes.csv", "r",encoding='utf-8', newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    # Pasar los datos a la plantilla HTML
    context = {
        'clientes_atendidos': clientes_atendidos,
        'csv_data': csv_data,
    }
    # Devolver una respuesta HTTP (puede ser una página de confirmación)
    return render(request, 'turnos_app/imprimir_datos.html', context)




def enviar_correo_atencion(request):
    if request.method == 'POST':
        subject = 'Informe de turnos'
        message =  'Turnos del día: ' + str(ahora)
        # Renderiza el template del correo
        template = render_to_string('turnos_app/email_template.html', {
            'email': 'santequera@wailus.co',
            'subject':subject,
            'message':message
            
        })

        # Crea un objeto EmailMessage
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['santequera@wailus.co'],
        )

        # Adjunta el archivo CSV
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'datos_clientes.csv') 
        if os.path.exists(csv_file_path):
            email.attach_file(csv_file_path, 'text/csv')

        email.fail_silently = False
        email.send()

        return redirect('lista_turnos')

    return HttpResponse('Método no permitido', status=405)


fech = str(ahora)
    
def obtener_lista_turnos(request):
    # Obtiene los datos más recientes de la lista de turnos (puedes personalizar esta parte)
    turnos = Turno.objects.all().values('nombre_cliente', 'referencia_motocicleta', 'numero_telefono', 'motivo_reparacion')
    numturnos = turnos
    # Convierte los datos en una lista de diccionarios
    lista_turnos = list(turnos)

    # Devuelve los datos en formato JSON
    return JsonResponse({'turnos': lista_turnos})


def reiniciar_numeros_de_turno(request):
    # Eliminar todos los registros de turnos existentes
    Turno.objects.all().delete()

    # Borrar los registros del archivo CSV
    csv_file_path = 'datos_clientes.csv'  # Ruta al archivo CSV
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows([])  # Escribe una lista vacía para borrar todos los registros
    else:
        # El archivo CSV no existe, puedes manejarlo de acuerdo a tus necesidades
        pass

    # Redirigir a la página deseada después de reiniciar
    return redirect('lista_turnos')  # Cambia 'pagina_principal' por el nombre de tu URL