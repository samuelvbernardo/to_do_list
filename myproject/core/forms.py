from django import forms
from .models import Tarefa

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'status', 'data_limite']
        widgets = {
            'data_limite': forms.DateInput(attrs={'type': 'date'})
        }