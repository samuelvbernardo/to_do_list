from django.contrib import admin
from .models import Tarefa, Projeto, Categoria, PerfilUsuario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cor', 'total_tarefas']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']
    
    def total_tarefas(self, obj):
        return obj.tarefas.count()
    total_tarefas.short_description = 'Total de Tarefas'


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'responsavel', 'status', 'data_inicio', 'data_fim', 'progresso']
    list_filter = ['status', 'data_criacao', 'data_inicio']
    search_fields = ['nome', 'descricao']
    date_hierarchy = 'data_criacao'
    filter_horizontal = ['membros']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'status')
        }),
        ('Equipe', {
            'fields': ('responsavel', 'membros')
        }),
        ('Prazos', {
            'fields': ('data_inicio', 'data_fim')
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def progresso(self, obj):
        return f"{obj.progresso}%"
    progresso.short_description = 'Progresso'


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'projeto', 'responsavel', 'status', 
        'prioridade', 'data_limite', 'atrasada_badge'
    ]
    list_filter = ['status', 'prioridade', 'projeto', 'data_criacao']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_criacao'
    filter_horizontal = ['categorias']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'data_conclusao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'projeto')
        }),
        ('Status e Prioridade', {
            'fields': ('status', 'prioridade')
        }),
        ('Atribuição', {
            'fields': ('responsavel', 'categorias')
        }),
        ('Prazos e Estimativas', {
            'fields': ('data_limite', 'estimativa_horas', 'horas_trabalhadas')
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao', 'data_conclusao'),
            'classes': ('collapse',)
        }),
    )
    
    def atrasada_badge(self, obj):
        if obj.atrasada:
            return '🔴 Atrasada'
        return '✅ No prazo'
    atrasada_badge.short_description = 'Status do Prazo'


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'cargo', 'departamento', 'telefone']
    search_fields = ['user__username', 'user__email', 'cargo', 'departamento']
    list_filter = ['departamento', 'cargo']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Profissionais', {
            'fields': ('cargo', 'departamento', 'telefone')
        }),
        ('Sobre', {
            'fields': ('bio', 'foto')
        }),
    )
