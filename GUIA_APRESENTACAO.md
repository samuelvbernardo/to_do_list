# 🎤 Guia de Apresentação do Projeto

## Roteiro Sugerido para Demonstração (10-15 minutos)

### 1. Introdução (2 minutos)

**O que dizer:**
- "Apresento o **TaskManager**, um sistema completo de gestão de tarefas e projetos"
- "Contexto: Área de Gestão de Projetos e Produtividade Empresarial"
- "Solução para empresas que precisam organizar projetos e gerenciar equipes"

**Mostrar:**
- Tela de login profissional
- README.md com documentação completa

### 2. Demonstração de Autenticação (2 minutos)

**Fluxo:**
1. Fazer login como usuário existente
2. Mostrar redirecionamento para Dashboard
3. Destacar menu de navegação
4. Mostrar dropdown do usuário (perfil, logout)

**Pontos a destacar:**
- "Sistema completo de autenticação com Django"
- "LoginRequiredMixin em todas as views protegidas"
- "Controle de permissões por usuário"

### 3. Dashboard - Estatísticas (2 minutos)

**Mostrar:**
- Cards com estatísticas (projetos, tarefas, pendentes, atrasadas)
- Projetos recentes
- Tarefas urgentes

**Pontos a destacar:**
- "Dashboard dinâmico com ORM do Django"
- "Queries otimizadas com select_related e prefetch_related"
- "Cálculo de progresso em tempo real"

### 4. CRUD de Projetos (3 minutos)

**Demonstrar:**
1. **Listar:** Mostrar filtros (status, busca, ordenação) e paginação
2. **Criar:** Criar novo projeto com membros
3. **Detalhar:** Ver projeto com tarefas associadas e progresso
4. **Editar:** Alterar informações (mostrar UserPassesTestMixin)
5. **Excluir:** Mostrar confirmação (não executar)

**Pontos a destacar:**
- "CRUD completo com Class-Based Views"
- "ProjetoListView, CreateView, DetailView, UpdateView, DeleteView"
- "Relacionamento ManyToMany com usuários (membros)"
- "Filtros e paginação implementados"

### 5. CRUD de Tarefas (3 minutos)

**Demonstrar:**
1. **Listar:** Filtros múltiplos (status, prioridade, projeto)
2. **Criar:** Nova tarefa com:
   - Projeto associado (ForeignKey)
   - Responsável (ForeignKey)
   - Múltiplas categorias (ManyToMany)
   - Prioridade e data limite
3. **Detalhar:** Ver tarefa completa com indicador de atraso
4. **Visualizar:** Tarefa atrasada destacada em vermelho

**Pontos a destacar:**
- "TarefaListView com filtros complexos usando Q objects"
- "Relacionamentos: ForeignKey (Projeto, User) e ManyToMany (Categorias)"
- "Formulários customizados com filtros dinâmicos"
- "Property `atrasada` calculada automaticamente"

### 6. Categorias e Perfil (1 minuto)

**Mostrar rapidamente:**
- Lista de categorias com cores
- Formulário de perfil do usuário (OneToOne com User)

**Pontos a destacar:**
- "4 modelos implementados com todos os tipos de relacionamento"
- "OneToOne: PerfilUsuario ↔ User"

### 7. Admin do Django (1 minuto)

**Mostrar:**
- Painel admin customizado
- ModelAdmin com list_display, list_filter, search_fields
- Fieldsets organizados
- Inline editing (opcional)

**Pontos a destacar:**
- "Admin completamente customizado"
- "Facilitando gestão pelo administrador"

### 8. Código e Arquitetura (2 minutos)

**Abrir arquivos:**
1. **models.py:** Mostrar os 4 modelos e relacionamentos
2. **views.py:** Mostrar CBVs (destacar que NÃO há FBVs)
3. **settings.py:** Mostrar configuração PostgreSQL

**Pontos a destacar:**
- "100% Class-Based Views - ZERO FBVs"
- "PostgreSQL configurado (SQLite NÃO usado)"
- "Código limpo, organizado e documentado"
- "Seguindo padrão MVT do Django"

## 🎯 Checklist Antes da Apresentação

### Preparação do Ambiente
- [ ] PostgreSQL rodando
- [ ] Banco de dados populado com dados de exemplo
- [ ] Servidor Django iniciado (`python manage.py runserver`)
- [ ] Browser aberto em abas:
  - [ ] http://localhost:8000/ (login)
  - [ ] http://localhost:8000/admin/
  - [ ] Documentação (README.md)

### Dados de Teste
- [ ] Pelo menos 3 usuários cadastrados
- [ ] 3-5 projetos criados
- [ ] 8-10 tarefas variadas
- [ ] Categorias coloridas
- [ ] Algumas tarefas atrasadas (para demonstração)

### Arquivos a Ter Abertos no Editor
- [ ] `core/models.py` - Para mostrar os modelos
- [ ] `core/views.py` - Para mostrar CBVs
- [ ] `myproject/settings.py` - Para mostrar PostgreSQL
- [ ] `README.md` - Para mostrar documentação

## 💡 Dicas de Apresentação

### O que ENFATIZAR
✅ "Todos os requisitos foram atendidos"
✅ "100% Class-Based Views"
✅ "PostgreSQL como banco de dados"
✅ "4 modelos com relacionamentos ForeignKey, ManyToMany e OneToOne"
✅ "Sistema completo de autenticação e autorização"
✅ "Filtros, ordenação e paginação implementados"
✅ "Código limpo e bem organizado"

### O que DEMONSTRAR
✅ Funcionalidades realmente funcionando (não só mostrar código)
✅ Responsividade (redimensionar janela)
✅ Filtros e buscas em ação
✅ Paginação funcionando
✅ Mensagens de feedback
✅ Validação de formulários

### O que EVITAR
❌ Não diga "faltou implementar..."
❌ Não mostre erros ou bugs
❌ Não use dados de teste não realistas
❌ Não demore muito em uma única funcionalidade

## 🗣️ Perguntas Esperadas e Respostas

### "Por que escolheu CBVs ao invés de FBVs?"
**Resposta:** "As CBVs são mais apropriadas para este projeto pois:
- Reutilizam código através de herança
- São mais organizadas e seguem DRY
- Facilitam manutenção
- São o padrão moderno do Django
- Atendem o requisito da avaliação"

### "Como funciona o relacionamento ManyToMany?"
**Resposta:** "Implementei ManyToMany em:
- Projeto ↔ Membros (um projeto pode ter vários membros, um usuário pode participar de vários projetos)
- Tarefa ↔ Categorias (uma tarefa pode ter várias categorias, uma categoria pode ter várias tarefas)
O Django cria automaticamente uma tabela intermediária"

### "Como funciona a paginação?"
**Resposta:** "Usei o atributo `paginate_by` nas CBVs ListView. Por exemplo:
- `paginate_by = 10` na ProjetoListView
- Django automaticamente divide os resultados
- Template recebe `page_obj` para navegação"

### "Como implementou os filtros?"
**Resposta:** "Sobrescrevi o método `get_queryset()` nas views:
- Pego parâmetros do GET request
- Aplico filtros usando ORM do Django
- Uso Q objects para queries complexas
- Exemplo: filtrar tarefas do usuário OU projetos que ele participa"

### "Por que PostgreSQL?"
**Resposta:** "PostgreSQL é:
- Requisito obrigatório da avaliação
- Banco relacional robusto
- Suporta melhor queries complexas
- Usado em produção em empresas reais
- Melhor que SQLite para aplicações multi-usuário"

## 📊 Estrutura de Demonstração por Requisito

| Requisito | Como Demonstrar | Arquivo para Abrir |
|-----------|-----------------|-------------------|
| CBVs | Abrir `views.py`, mostrar classes | `core/views.py` |
| CRUD | Navegar pelas telas do sistema | Browser |
| PostgreSQL | Mostrar `settings.py` e conectar no admin | `settings.py` |
| Autenticação | Login/Logout, criar usuário | Browser |
| 4 Modelos | Abrir `models.py` | `core/models.py` |
| Relacionamentos | Explicar com diagrama ou código | `models.py` |
| Filtros/Paginação | Usar filtros na interface | Browser |
| Interface | Navegar pelo sistema | Browser |

## 🎬 Ordem Sugerida de Telas

1. Login → Dashboard
2. Projetos → Criar → Ver Detalhes
3. Tarefas → Filtrar → Ver Detalhes
4. Categorias (rápido)
5. Perfil (rápido)
6. Admin
7. Código (models.py, views.py)

## ⏱️ Distribuição do Tempo

- Introdução: 2 min
- Login e Dashboard: 2 min
- CRUD Projetos: 3 min
- CRUD Tarefas: 3 min
- Outros (Categorias, Perfil): 1 min
- Admin: 1 min
- Código: 2 min
- **Perguntas:** 1-2 min

**Total:** ~15 minutos

## 🚀 Script de Última Hora

Se tiver pouco tempo antes da apresentação:

```powershell
# 1. Ativar ambiente virtual
cd myproject
..\venv\Scripts\activate

# 2. Popular banco de dados
python manage.py shell < populate_db.py

# 3. Iniciar servidor
python manage.py runserver

# 4. Abrir browser em:
# - http://localhost:8000/
# - http://localhost:8000/admin/

# 5. Testar login com usuários de exemplo
# Usuário: maria.silva | Senha: senha123
```

## ✅ Checklist Final (1 minuto antes)

- [ ] Servidor rodando sem erros
- [ ] Browser com abas preparadas
- [ ] Editor com arquivos abertos
- [ ] Dados de teste carregados
- [ ] Credenciais de login anotadas
- [ ] Documentação visível (README aberto)
- [ ] Confiança e conhecimento do projeto ✨

---

**Boa sorte! 🍀 Você está preparado(a)!**
