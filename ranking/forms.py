from django.forms import ModelForm
from .models import Comentario

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = [
            'author',
            'text',
            'nota',
        ]
        labels = {
            'author': 'Usuário',
            'text': 'Texto',
            'nota': 'Nota',
        }
