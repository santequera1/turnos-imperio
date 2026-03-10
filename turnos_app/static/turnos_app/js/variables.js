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
esperar()
const text2 = `Repito, Llamando a ${nombreCliente}`
const utterThis2 = new SpeechSynthesisUtterance(text2)
synth.speak(utterThis2)
fire(nombreCliente)
}


function fire(nombreCliente) {
    Swal.fire({
      position: 'top-end',
      icon: 'warning',
      title: `Llamando a ${nombreCliente}`,
      showConfirmButton: false,
      timer: 5000
    });
  }


 function esperar (){ setTimeout(function () {
    console.log("HOLA")
  }, 2500);}

/*function miFunc(nombreCliente) {
    Swal.fire({
      position: 'top-end',
      icon: 'success',
      title: `Llamando a ${nombreCliente}`,
      showConfirmButton: false,
      timer: 5000
    });
  }
*/

/** 
 // Empezamos utilizando el sintetizador de voz 👅
const synth = window.speechSynthesis
const text = 'Hola, esta es una prueba'
const utterThis = new SpeechSynthesisUtterance(text)
// Cambiamos el valor del tono (por defecto 1)
utterThis.pitch = 1.22
// Cambiamos el valor de la velocidad (por defecto 1)
utterThis.rate = 1.55
synth.speak(utterThis)
*/



  