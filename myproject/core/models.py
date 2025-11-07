from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    cor = models.CharField(max_length=7, default='#007bff', verbose_name="Cor (hex)")
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Projeto(models.Model):
    STATUS_CHOICES = [
        ('PLANEJAMENTO', 'Planejamento'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome do Projeto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PLANEJAMENTO', 
        verbose_name="Status"
    )
    responsavel = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='projetos_responsavel',
        verbose_name="Responsável"
    )
    membros = models.ManyToManyField(
        User, 
        related_name='projetos_membro', 
        blank=True,
        verbose_name="Membros"
    )
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(blank=True, null=True, verbose_name="Data de Término")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('projeto_detail', kwargs={'pk': self.pk})
    
    @property
    def total_tarefas(self):
        return self.tarefas.count()
    
    @property
    def tarefas_concluidas(self):
        return self.tarefas.filter(status='CONCLUIDA').count()
    
    @property
    def progresso(self):
        if self.total_tarefas == 0:
            return 0
        return int((self.tarefas_concluidas / self.total_tarefas) * 100)


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo")
    departamento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departamento")
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True, verbose_name="Foto")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDENTE', 
        verbose_name="Status"
    )
    prioridade = models.CharField(
        max_length=10, 
        choices=PRIORIDADE_CHOICES, 
        default='MEDIA',
        verbose_name="Prioridade"
    )
    
    # Relacionamentos
    projeto = models.ForeignKey(
        Projeto, 
        on_delete=models.CASCADE, 
        related_name='tarefas',
        verbose_name="Projeto"
    )
    responsavel = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='tarefas_responsavel',
        verbose_name="Responsável"
    )
    categorias = models.ManyToManyField(
        Categoria, 
        related_name='tarefas', 
        blank=True,
        verbose_name="Categorias"
    )
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    data_limite = models.DateField(blank=True, null=True, verbose_name="Data Limite")
    data_conclusao = models.DateTimeField(blank=True, null=True, verbose_name="Data de Conclusão")
    
    # Campos adicionais
    estimativa_horas = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="Estimativa (horas)"
    )
    horas_trabalhadas = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        verbose_name="Horas Trabalhadas"
    )
    
    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('tarefa_detail', kwargs={'pk': self.pk})
    
    @property
    def atrasada(self):
        from datetime import date
        if self.data_limite and self.status != 'CONCLUIDA':
            return date.today() > self.data_limite
        return False
