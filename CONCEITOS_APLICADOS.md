# 📚 Documentação Técnica - Conceitos Aplicados

## Aulas 09 e 10 - Conceitos Avançados Implementados

### 1. Class-Based Views (CBVs) Genéricas

#### ListView
Implementado em: `ProjetoListView`, `TarefaListView`, `CategoriaListView`

**Funcionalidades:**
- Paginação automática
- Filtros personalizados via `get_queryset()`
- Context data adicional via `get_context_data()`

```python
class TarefaListView(LoginRequiredMixin, ListView):
    model = Tarefa
    template_name = 'core/tarefa_list.html'
    context_object_name = 'tarefas'
    paginate_by = 15
    
    def get_queryset(self):
        # Filtros e ordenação personalizados
        queryset = Tarefa.objects.filter(...)
        return queryset
```

#### CreateView
Implementado em: `ProjetoCreateView`, `TarefaCreateView`, `CategoriaCreateView`

**Funcionalidades:**
- Formulários automáticos
- Validação integrada
- Redirecionamento após criação

#### UpdateView
Implementado em: `ProjetoUpdateView`, `TarefaUpdateView`, etc.

**Funcionalidades:**
- Edição de objetos existentes
- Pré-preenchimento automático
- Validação e salvamento

#### DeleteView
Implementado em: `ProjetoDeleteView`, `TarefaDeleteView`, etc.

**Funcionalidades:**
- Confirmação de exclusão
- Redirecionamento configurável
- Mensagens de sucesso

#### DetailView
Implementado em: `ProjetoDetailView`, `TarefaDetailView`

**Funcionalidades:**
- Visualização detalhada
- Context data relacionado
- Navegação facilitada

### 2. Mixins de Autenticação

#### LoginRequiredMixin
Aplicado em **TODAS** as views protegidas

```python
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    # ...
```

#### UserPassesTestMixin
Usado para controle de permissões

```python
class ProjetoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        projeto = self.get_object()
        return self.request.user == projeto.responsavel
```

### 3. ORM Avançada do Django

#### Relacionamentos Complexos

**ForeignKey (Muitos-para-Um)**
```python
class Tarefa(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL)
```

**ManyToManyField (Muitos-para-Muitos)**
```python
class Projeto(models.Model):
    membros = models.ManyToManyField(User, related_name='projetos_membro')

class Tarefa(models.Model):
    categorias = models.ManyToManyField(Categoria, related_name='tarefas')
```

**OneToOneField (Um-para-Um)**
```python
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
```

#### Otimização de Queries

**select_related()** - Para ForeignKey
```python
queryset = Tarefa.objects.select_related('projeto', 'responsavel')
```

**prefetch_related()** - Para ManyToMany
```python
queryset = Tarefa.objects.prefetch_related('categorias')
```

#### Filtros Complexos com Q Objects
```python
from django.db.models import Q

queryset = Tarefa.objects.filter(
    Q(responsavel=user) | Q(projeto__membros=user)
).distinct()
```

#### Agregação e Anotação
```python
@property
def total_tarefas(self):
    return self.tarefas.count()

@property
def progresso(self):
    if self.total_tarefas == 0:
        return 0
    return int((self.tarefas_concluidas / self.total_tarefas) * 100)
```

### 4. Sistema de Autenticação Completo

#### Views Customizadas
```python
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
```

#### Formulário de Registro
```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # Criação automática de perfil
    def save(self, commit=True):
        user = super().save(commit=False)
        # ...
        PerfilUsuario.objects.create(user=user)
```

#### Configurações de Autenticação
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
```

### 5. Formulários Personalizados

#### ModelForms Avançados
```python
class TarefaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar projetos do usuário
        if self.user:
            self.fields['projeto'].queryset = Projeto.objects.filter(
                Q(responsavel=self.user) | Q(membros=self.user)
            ).distinct()
```

#### Widgets Customizados
```python
widgets = {
    'data_limite': forms.DateInput(attrs={'type': 'date'}),
    'cor': forms.TextInput(attrs={'type': 'color'}),
    'descricao': forms.Textarea(attrs={'rows': 4}),
}
```

### 6. Admin Customizado

#### ModelAdmin Avançado
```python
@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'projeto', 'status', 'prioridade']
    list_filter = ['status', 'prioridade', 'projeto']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_criacao'
    filter_horizontal = ['categorias']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {'fields': (...)}),
        ('Status e Prioridade', {'fields': (...)}),
    )
```

### 7. Paginação Implementada

```python
class ProjetoListView(ListView):
    paginate_by = 10  # 10 itens por página
```

**Template:**
```django
{% if is_paginated %}
    <nav>
        <ul class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page={{ page_obj.previous_page_number }}">Anterior</a>
            {% endif %}
            <!-- ... -->
        </ul>
    </nav>
{% endif %}
```

### 8. Mensagens do Django

```python
from django.contrib import messages

def form_valid(self, form):
    messages.success(self.request, 'Projeto criado com sucesso!')
    return super().form_valid(form)
```

**Configuração:**
```python
MESSAGE_TAGS = {
    messages.SUCCESS: 'success',
    messages.ERROR: 'danger',
}
```

### 9. Signals (Conceito Extra)

Possível implementação futura:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)
```

### 10. Context Processors (Conceito Extra)

Dados globais em todos os templates:
```python
def user_context(request):
    if request.user.is_authenticated:
        return {
            'total_tarefas_pendentes': Tarefa.objects.filter(
                responsavel=request.user,
                status='PENDENTE'
            ).count()
        }
    return {}
```

## 🎯 Boas Práticas Aplicadas

1. **DRY (Don't Repeat Yourself)**
   - Uso de CBVs genéricas
   - Templates com herança
   - Formulários reutilizáveis

2. **MVT Pattern**
   - Models com lógica de negócio
   - Views apenas para coordenação
   - Templates para apresentação

3. **Segurança**
   - CSRF Protection
   - LoginRequired em views
   - Validação de formulários
   - Escape automático de HTML

4. **Performance**
   - select_related() e prefetch_related()
   - Paginação
   - Índices no banco (implicit via ForeignKey)

5. **Manutenibilidade**
   - Código documentado
   - Nomenclatura clara
   - Separação de responsabilidades
   - Admin bem configurado

## 📈 Próximas Melhorias Possíveis

1. **API REST** com Django REST Framework
2. **WebSockets** para notificações em tempo real
3. **Celery** para tarefas assíncronas
4. **Testes Automatizados** (unitários e integração)
5. **Docker** para containerização
6. **CI/CD** com GitHub Actions
7. **Relatórios** em PDF
8. **Gráficos** com Chart.js
9. **Comentários** em tarefas
10. **Histórico de alterações**

---

Este documento demonstra a aplicação prática dos conceitos avançados de Django, atendendo plenamente aos requisitos das Aulas 09 e 10.
