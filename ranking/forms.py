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
            'text': 'Texto',
            'nota': 'Nota',
        }
