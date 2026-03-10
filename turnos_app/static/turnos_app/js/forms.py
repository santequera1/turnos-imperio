from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre_cliente', 'referencia_motocicleta', 'numero_telefono','motivo_reparacion']

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)

        # Agrega clases CSS personalizadas a las etiquetas <label>
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs.update({
                'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50',
            })

        # Agrega clases CSS personalizadas a los campos de entrada <input>
        self.fields['nombre_cliente'].widget.attrs.update({
            'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50',
        })
        self.fields['referencia_motocicleta'].widget.attrs.update({
            'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50',
        })
        self.fields['numero_telefono'].widget.attrs.update({
            'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50',
        })
        self.fields['motivo_reparacion'].widget.attrs.update({
            'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50',
        })


class ReiniciarNumerosForm(forms.Form):
    reiniciar = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
