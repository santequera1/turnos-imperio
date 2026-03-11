from django import forms
from .models import Turno, ClienteFrecuente

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'referencia_motocicleta', 'numero_telefono', 'motivo_reparacion', 'cliente_frecuente']

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)

        # Agregar clases CSS personalizadas a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50',
            })

        # Hacer el campo numero_telefono obligatorio
        self.fields['numero_telefono'].required = True


class ReiniciarNumerosForm(forms.Form):
    reiniciar = forms.BooleanField(widget=forms.HiddenInput(), initial=True)