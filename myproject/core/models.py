from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONCLUIDA', 'Concluída'),
    ]
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    data_limite = models.DateField(blank=True, null=True, verbose_name="Data limite")

    def __str__(self):
        return self.titulo
