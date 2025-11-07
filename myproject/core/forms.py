from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tarefa, Projeto, Categoria, PerfilUsuario


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label="Nome")
    last_name = forms.CharField(max_length=150, required=True, label="Sobrenome")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirmação de senha',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Criar perfil automaticamente
            PerfilUsuario.objects.create(user=user)
        return user


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'status', 'membros', 'data_inicio', 'data_fim']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do projeto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada do projeto'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'membros': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Projeto',
            'descricao': 'Descrição',
            'status': 'Status',
            'membros': 'Membros da Equipe',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Término (opcional)',
        }


class TarefaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar projetos disponíveis para o usuário
        if self.user:
            from django.db.models import Q
            self.fields['projeto'].queryset = Projeto.objects.filter(
                Q(responsavel=self.user) | Q(membros=self.user)
            ).distinct()
            
            self.fields['responsavel'].queryset = User.objects.filter(
                Q(projetos_responsavel__in=self.fields['projeto'].queryset) |
                Q(projetos_membro__in=self.fields['projeto'].queryset)
            ).distinct()
    
    class Meta:
        model = Tarefa
        fields = [
            'titulo', 'descricao', 'projeto', 'status', 'prioridade',
            'responsavel', 'categorias', 'data_limite', 
            'estimativa_horas', 'horas_trabalhadas'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da tarefa'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada'}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
            'data_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estimativa_horas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'horas_trabalhadas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
        }
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'projeto': 'Projeto',
            'status': 'Status',
            'prioridade': 'Prioridade',
            'responsavel': 'Responsável',
            'categorias': 'Categorias',
            'data_limite': 'Data Limite',
            'estimativa_horas': 'Estimativa (horas)',
            'horas_trabalhadas': 'Horas Trabalhadas',
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'cor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da categoria'}),
            'cor': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        }
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'cor': 'Cor',
        }


class PerfilUsuarioForm(forms.ModelForm):
    # Campos adicionais do User
    first_name = forms.CharField(max_length=150, required=False, label="Nome")
    last_name = forms.CharField(max_length=150, required=False, label="Sobrenome")
    email = forms.EmailField(required=False, label="E-mail")
    
    class Meta:
        model = PerfilUsuario
        fields = ['telefone', 'cargo', 'departamento', 'bio']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Desenvolvedor'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: TI'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Fale um pouco sobre você...'}),
        }
        labels = {
            'telefone': 'Telefone',
            'cargo': 'Cargo',
            'departamento': 'Departamento',
            'bio': 'Biografia',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        perfil = super().save(commit=False)
        
        # Atualizar campos do User
        if perfil.user:
            perfil.user.first_name = self.cleaned_data.get('first_name', '')
            perfil.user.last_name = self.cleaned_data.get('last_name', '')
            perfil.user.email = self.cleaned_data.get('email', '')
            if commit:
                perfil.user.save()
        
        if commit:
            perfil.save()
        
        return perfil