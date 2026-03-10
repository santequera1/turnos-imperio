//Obteniendo datos del formulario
$( document ).ready(function() {
  console.log( "ready!" );
  var nombre = $("#id_nombre_cliente").val();
  var moto = $("#id_referencia_motocicleta").val();
  var telefono = $("#id_numero_telefono").val();
  var motivo = $("#id_motivo_reparacion").val();


  //invocando funcion limpiar
  limpiar();
});


//Funcion para limpiar los campos sin borrar los datos de local storage
function limpiar(){
  $("#id_nombre_cliente").val("");
  $("#id_referencia_motocicleta").val("");
  $("#id_numero_telefono").val("");
  $("#id_motivo_reparacion").val("");
  $("#id_nombre_cliente").focus();
  

}



$(document).on("change", "input[type='checkbox']", function () {
	$(this).parent()[this.checked ? "addClass" : "removeClass"]("checked");
});

const checkboxes = document.querySelectorAll('.checkbox');
    const turnosAtendiendo = [];

    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', function () {
            const listItem = this.parentElement;
            const turnoId = this.value;
            
            if (this.checked) {
                listItem.classList.add('selected');
                turnosAtendiendo.push(turnoId);
            } else {
                listItem.classList.remove('selected');
                const index = turnosAtendiendo.indexOf(turnoId);
                if (index !== -1) {
                    turnosAtendiendo.splice(index, 1);
                }
            }

            // Enviar la lista de IDs a la página lista-turnos.html
            const turnosAtendiendoInput = document.getElementById('turnos-atendiendo-input');
            turnosAtendiendoInput.value = JSON.stringify(turnosAtendiendo);
        });
    });



    function confirmarBorrado() {
        if (confirm("¿Estás seguro de que deseas borrar todos los registros?")) {
            window.location.href = "{% url 'lista-turnos' %}";  // Redirige si se confirma
        }
    }

    
    

    


