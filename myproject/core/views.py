from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.contrib import messages
from .models import Tarefa, Projeto, Categoria, PerfilUsuario
from .forms import (
    TarefaForm, ProjetoForm, CategoriaForm, 
    CustomUserCreationForm, PerfilUsuarioForm
)


# Autenticação
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha inválidos.')
        return super().form_invalid(form)


class RegistroView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'core/registro.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return response


# Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Estatísticas gerais
        context['total_projetos'] = Projeto.objects.filter(
            Q(responsavel=user) | Q(membros=user)
        ).distinct().count()
        
        context['total_tarefas'] = Tarefa.objects.filter(
            Q(responsavel=user) | Q(projeto__membros=user)
        ).distinct().count()
        
        context['tarefas_pendentes'] = Tarefa.objects.filter(
            Q(responsavel=user) | Q(projeto__membros=user),
            status='PENDENTE'
        ).distinct().count()
        
        context['tarefas_atrasadas'] = Tarefa.objects.filter(
            Q(responsavel=user) | Q(projeto__membros=user),
            status__in=['PENDENTE', 'EM_ANDAMENTO'],
            data_limite__lt=timezone.now().date()
        ).distinct().count()
        
        # Projetos recentes
        context['projetos_recentes'] = Projeto.objects.filter(
            Q(responsavel=user) | Q(membros=user)
        ).distinct().order_by('-data_criacao')[:5]
        
        # Tarefas urgentes
        context['tarefas_urgentes'] = Tarefa.objects.filter(
            Q(responsavel=user) | Q(projeto__membros=user),
            prioridade__in=['ALTA', 'URGENTE'],
            status__in=['PENDENTE', 'EM_ANDAMENTO']
        ).distinct().order_by('-prioridade', 'data_limite')[:10]
        
        return context


# Projetos
class ProjetoListView(LoginRequiredMixin, ListView):
    model = Projeto
    template_name = 'core/projeto_list.html'
    context_object_name = 'projetos'
    paginate_by = 10
    login_url = 'login'
    
    def get_queryset(self):
        queryset = Projeto.objects.filter(
            Q(responsavel=self.request.user) | Q(membros=self.request.user)
        ).distinct()
        
        # Filtro por status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Busca por nome
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | Q(descricao__icontains=busca)
            )
        
        # Ordenação
        ordem = self.request.GET.get('ordem', '-data_criacao')
        queryset = queryset.order_by(ordem)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Projeto.STATUS_CHOICES
        return context


class ProjetoDetailView(LoginRequiredMixin, DetailView):
    model = Projeto
    template_name = 'core/projeto_detail.html'
    context_object_name = 'projeto'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projeto = self.get_object()
        context['tarefas'] = projeto.tarefas.select_related('responsavel').prefetch_related('categorias')
        return context


class ProjetoCreateView(LoginRequiredMixin, CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'core/projeto_form.html'
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.responsavel = self.request.user
        messages.success(self.request, 'Projeto criado com sucesso!')
        return super().form_valid(form)


class ProjetoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'core/projeto_form.html'
    login_url = 'login'
    
    def test_func(self):
        projeto = self.get_object()
        return self.request.user == projeto.responsavel
    
    def form_valid(self, form):
        messages.success(self.request, 'Projeto atualizado com sucesso!')
        return super().form_valid(form)


class ProjetoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Projeto
    template_name = 'core/projeto_confirm_delete.html'
    success_url = reverse_lazy('projeto_list')
    login_url = 'login'
    
    def test_func(self):
        projeto = self.get_object()
        return self.request.user == projeto.responsavel
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Projeto excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# Tarefas
class TarefaListView(LoginRequiredMixin, ListView):
    model = Tarefa
    template_name = 'core/tarefa_list.html'
    context_object_name = 'tarefas'
    paginate_by = 15
    login_url = 'login'
    
    def get_queryset(self):
        queryset = Tarefa.objects.filter(
            Q(responsavel=self.request.user) | Q(projeto__membros=self.request.user)
        ).select_related('projeto', 'responsavel').prefetch_related('categorias').distinct()
        
        # Filtro por status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filtro por prioridade
        prioridade = self.request.GET.get('prioridade')
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade)
        
        # Filtro por projeto
        projeto_id = self.request.GET.get('projeto')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
        
        # Busca
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(titulo__icontains=busca) | Q(descricao__icontains=busca)
            )
        
        # Ordenação
        ordem = self.request.GET.get('ordem', '-data_criacao')
        queryset = queryset.order_by(ordem)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Tarefa.STATUS_CHOICES
        context['prioridade_choices'] = Tarefa.PRIORIDADE_CHOICES
        context['projetos'] = Projeto.objects.filter(
            Q(responsavel=self.request.user) | Q(membros=self.request.user)
        ).distinct()
        return context


class TarefaDetailView(LoginRequiredMixin, DetailView):
    model = Tarefa
    template_name = 'core/tarefa_detail.html'
    context_object_name = 'tarefa'
    login_url = 'login'


class TarefaCreateView(LoginRequiredMixin, CreateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = 'core/tarefa_form.html'
    login_url = 'login'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if not form.instance.responsavel:
            form.instance.responsavel = self.request.user
        messages.success(self.request, 'Tarefa criada com sucesso!')
        return super().form_valid(form)


class TarefaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = 'core/tarefa_form.html'
    login_url = 'login'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Tarefa atualizada com sucesso!')
        return super().form_valid(form)


class TarefaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarefa
    template_name = 'core/tarefa_confirm_delete.html'
    success_url = reverse_lazy('tarefa_list')
    login_url = 'login'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tarefa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# Categorias
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'core/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 20
    login_url = 'login'


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('categoria_list')
    login_url = 'login'
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoria criada com sucesso!')
        return super().form_valid(form)


class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('categoria_list')
    login_url = 'login'
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada com sucesso!')
        return super().form_valid(form)


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'core/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')
    login_url = 'login'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoria excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# Perfil
class PerfilUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = 'core/perfil_form.html'
    success_url = reverse_lazy('dashboard')
    login_url = 'login'
    
    def get_object(self, queryset=None):
        # Cria perfil automaticamente se não existir
        perfil, created = PerfilUsuario.objects.get_or_create(user=self.request.user)
        return perfil
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


# Importar timezone para usar no DashboardView
from django.utils import timezone
