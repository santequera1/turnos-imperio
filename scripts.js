var telefono = document.getElementById("telefono_cliente");
var nombre_cliente = document.getElementById("nombre_cliente");
var moto_cliente = document.getElementById("motocicleta_cliente");
var placa = document.getElementById("placa");


// Obtener el texto del elemento
var numeroSinPrefijo = telefono.textContent;
var textoSinEspacios = numeroSinPrefijo.trim();

var nombreEspacios = nombre_cliente.textContent;
var nombreSinEspacios = nombreEspacios.trim();

var motoEspacios = moto_cliente.textContent;
var motoSinEspacios = motoEspacios.trim();

var placaespacios = placa.textContent;
var placasinespacios = placaespacios.trim();

console.log(textoSinEspacios);
console.log(nombreSinEspacios);
console.log(motoSinEspacios);
console.log(placasinespacios);

document.getElementById('enviar-sms').addEventListener('click', function() {
    // Agrega tus credenciales de Twilio y otros detalles aquí
    const accountSid = '';
    const authToken = '';
    var url = document.URL;
    // Número de teléfono Twilio (debe ser un número verificado)
    const from = '+19285850221';

    // Número de destino
    var to = "+57" + textoSinEspacios;

    const messageBody = 'Hola ' + nombreSinEspacios + "Tienes un informe para tu motocicleta, Haz click en el siguiente link para ver la información completa: " + url;

    // Configura la solicitud POST
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://api.twilio.com/2010-04-01/Accounts/' + accountSid + '/Messages.json');
    xhr.setRequestHeader('Authorization', 'Basic ' + btoa(accountSid + ':' + authToken));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Datos del mensaje
    const data = new URLSearchParams();
    data.append('From', from);
    data.append('To', to);
    data.append('Body', messageBody);

    // Manejar la respuesta
    xhr.onload = function() {
        if (xhr.status === 201) {
            console.log('Mensaje enviado con éxito:', xhr.responseText);
        } else {
            console.error('Error al enviar el mensaje:', xhr.responseText);
        }
    };

    // Enviar la solicitud
    xhr.send(data);
});