from django import forms
from django.forms import ModelForm
from .models import Comentario, Nota

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = [
            'text',
            'nota',
        ]
        labels = {
            'text': 'Comentário',
            'nota': 'Nota',
        }
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'nota': forms.HiddenInput(attrs={"id":"nota_input", "name":"nota", "value":""}),
        }

class ComentarioUpdateForm(ModelForm):
    class Meta:
        model = Comentario
        fields = [
            'text',
        ]
        labels = {
            'text': 'Comentário',
        }
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Opcional'}),
        }
