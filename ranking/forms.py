from django import forms
from django.forms import ModelForm
from .models import Comentario

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
