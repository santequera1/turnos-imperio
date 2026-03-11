let numeroDeTurnos = 0;  // Inicializa el número de turnos
let numeromenor = numeroDeTurnos - 1;
var llamar = document.getElementById("boton-alerta");
let actualizacionEnProgreso = false; // Variable para rastrear si la actualización está en curso

let primerTurnoDetectado = false;  // Variable para controlar si se ha detectado el primer turno
var mismapagina = document.URL;
const reiniciar = 0;
var llamar = document.getElementById("boton-alerta");




function primerTurno() {
    Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: `Primer turno`,
        text: `Esperando mas turnos`,
        showConfirmButton: false,
        timer: 5000
    });

    
    // Por ejemplo, después de 10 segundos, mostrar otro mensaje
    setTimeout(function () {
        Swal.fire({
            position: 'top-end',
            icon: 'info',
            title: `Esperando segundo turno...`,
            text: '.',
            showConfirmButton: false,
            timer: 5000
        });
    }, 10000);
}


var audio = new Audio("/static/turnos_app/js/turnosound.mp3");
function sonar(audio){
    var audio = new Audio("/static/turnos_app/js/turnosound.mp3");
    audio.play();
}

var nuevoturno = new Boolean(false);
function agendado() {
  navigator.vibrate(1000);
  Swal.fire({
    position: 'top-end',
    icon: 'success',
    title: `Nuevo turno`,
    showConfirmButton: false,
    timer: 5000
  })

  sonar(audio)

  // Esperar 4 segundos (4000 milisegundos) antes de recargar la página
  setTimeout(function () {
    location.reload();
  }, 2500);
}

  function terminado() {
    Swal.fire({
      position: 'top-end',
      icon: 'success',
      title: `Finalizó un turno`,
      showConfirmButton: false,
      timer: 5000
    });


  // Esperar 4 segundos (4000 milisegundos) antes de recargar la página
  setTimeout(function () {
    location.reload();
  }, 2500);
}

function miFunc(nombreCliente){
    // Empezamos utilizando el sintetizador de voz 👅
const synth = window.speechSynthesis
const text = `Llamando a ${nombreCliente}`
const utterThis = new SpeechSynthesisUtterance(text)
// Cambiamos el valor del tono (por defecto 1)
utterThis.pitch = 1
// Cambiamos el valor de la velocidad (por defecto 1)
utterThis.rate = 0.93
synth.speak(utterThis)
fire(nombreCliente)
}




const actualizarListaTurnos = () => {
    if (!actualizacionEnProgreso) { // Evitar que se ejecute si ya hay una actualización en curso
        actualizacionEnProgreso = true; // Marcar que la actualización está en curso
        fetch('/obtener-lista-turnos/')
            .then(response => response.json())
            .then(data => {
                console.log(data.turnos);

                if (data.turnos.length === 1 && !primerTurnoDetectado) {
                    primerTurno();
                    primerTurnoDetectado = true;
                } else if (data.turnos.length === numeroDeTurnos + 1) {
                    agendado();
                } else if (data.turnos.length === numeroDeTurnos - 1) {
                    terminado();
                } else {
                    console.log("No hay cambios en los turnos");
                }

                numeroDeTurnos = data.turnos.length;
            })
            .catch(error => {
                console.error('Error al obtener la lista de turnos:', error);
            })
            .finally(() => {
                actualizacionEnProgreso = false; // Marcar que la actualización ha terminado
            });
    }
};

// Llamando a la función de actualización al cargar la página
actualizarListaTurnos();

// Actualiza cada X segundos solo si no hay una actualización en curso
setInterval(actualizarListaTurnos, 3000);
