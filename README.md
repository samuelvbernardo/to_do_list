# TaskManager - Sistema de Gestão de Tarefas e Projetos

## 📋 Descrição do Projeto

Sistema completo de gestão de tarefas e projetos desenvolvido com Django, atendendo aos requisitos da avaliação da Segunda Unidade.

### Contexto de Mercado
**Área:** Gestão de Projetos e Produtividade Empresarial

O TaskManager é uma solução para empresas que precisam organizar projetos, delegar tarefas, acompanhar progresso e gerenciar equipes de forma eficiente.

## ✅ Requisitos Atendidos

### Frontend
- ✅ **HTML5 e CSS3:** Semântica correta, responsividade e boas práticas
- ✅ **Bootstrap 5:** Framework CSS responsivo
- ✅ **Design Moderno:** Interface intuitiva e agradável

### Backend (Django)
- ✅ **Estrutura MVT:** 100% Class-Based Views (CBVs)
- ✅ **CRUD Completo:** Implementado para Projetos, Tarefas e Categorias
- ✅ **ORM Avançada:** Filtros, ordenação, paginação e relacionamentos
- ✅ **PostgreSQL:** Banco de dados relacional obrigatório
- ✅ **Autenticação e Autorização:**
  - Sistema de login/logout
  - Registro de usuários
  - LoginRequiredMixin em todas as views protegidas
  - UserPassesTestMixin para controle de permissões
  - Restrições de acesso por responsável/membro do projeto

### Modelos (4 modelos com relacionamentos)
1. **Categoria** - Categorização de tarefas
2. **Projeto** - Agrupamento de tarefas
   - ForeignKey para User (responsável)
   - ManyToMany para User (membros)
3. **Tarefa** - Tarefas individuais
   - ForeignKey para Projeto
   - ForeignKey para User (responsável)
   - ManyToMany para Categoria
4. **PerfilUsuario** - Extensão do modelo User
   - OneToOne para User

## 🚀 Funcionalidades

### Dashboard
- Estatísticas em tempo real
- Visualização de projetos recentes
- Tarefas urgentes e atrasadas
- Ações rápidas

### Gestão de Projetos
- CRUD completo
- Controle de status e progresso
- Gestão de equipes (responsável + membros)
- Filtros e busca avançada
- Paginação

### Gestão de Tarefas
- CRUD completo
- Prioridades (Baixa, Média, Alta, Urgente)
- Status (Pendente, Em Andamento, Concluída, Cancelada)
- Controle de prazos
- Estimativa de horas
- Categorização múltipla
- Indicador de tarefas atrasadas

### Gestão de Categorias
- CRUD completo
- Cores personalizadas
- Organização visual

### Sistema de Usuários
- Registro de novos usuários
- Login/Logout
- Perfis personalizados
- Informações profissionais

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Django 5.2.6**
- **PostgreSQL** (banco de dados)
- **Bootstrap 5.3**
- **Bootstrap Icons**
- **HTML5 / CSS3**
- **JavaScript (ES6+)**

## 📦 Instalação e Configuração

### 1. Pré-requisitos
```bash
# Python 3.8 ou superior
# PostgreSQL 12 ou superior
# pip (gerenciador de pacotes Python)
```

### 2. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd to_do_list
```

### 3. Crie um Ambiente Virtual
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 4. Instale as Dependências
```powershell
pip install -r requirements.txt
```

### 5. Configure o PostgreSQL

**Opção 1: Instalar PostgreSQL localmente**
1. Baixe e instale o PostgreSQL: https://www.postgresql.org/download/
2. Crie um banco de dados:
```sql
CREATE DATABASE taskmanager_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE taskmanager_db TO postgres;
```

**Opção 2: Usar Docker**
```powershell
docker run --name postgres-taskmanager -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=taskmanager_db -p 5432:5432 -d postgres:15
```

### 6. Configure o Banco de Dados no Django

Edite `myproject/myproject/settings.py` se necessário:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanager_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',  # Altere para sua senha
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 7. Execute as Migrações
```powershell
cd myproject
python manage.py makemigrations
python manage.py migrate
```

### 8. Crie um Superusuário
```powershell
python manage.py createsuperuser
```

### 9. Execute o Servidor
```powershell
python manage.py runserver
```

### 10. Acesse o Sistema
- **Aplicação:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/

## 📖 Como Usar

### Primeiro Acesso
1. Acesse http://localhost:8000/
2. Clique em "Registre-se aqui"
3. Preencha os dados e crie sua conta
4. Faça login com suas credenciais

### Fluxo Recomendado
1. **Crie Categorias** (ex: Frontend, Backend, Design, Documentação)
2. **Crie um Projeto** (defina nome, descrição, datas, membros)
3. **Crie Tarefas** vinculadas ao projeto
4. **Acompanhe o progresso** no Dashboard

### Filtros e Buscas
- Use os filtros nas páginas de listagem
- Pesquise por título ou descrição
- Ordene por data, nome ou prioridade

## 🎨 Estrutura do Projeto

```
to_do_list/
├── myproject/
│   ├── core/                    # App principal
│   │   ├── models.py           # 4 modelos com relacionamentos
│   │   ├── views.py            # Class-Based Views
│   │   ├── forms.py            # Formulários customizados
│   │   ├── urls.py             # URLs do app
│   │   ├── admin.py            # Configuração do admin
│   │   ├── templates/core/     # Templates HTML5
│   │   └── static/core/        # CSS e JS
│   ├── myproject/              # Configurações
│   │   ├── settings.py         # PostgreSQL configurado
│   │   └── urls.py             # URLs principais
│   ├── manage.py
│   └── db.sqlite3              # (removido - usando PostgreSQL)
└── requirements.txt            # Dependências
```

## 🔐 Segurança

- Autenticação obrigatória para todas as páginas (exceto login/registro)
- CSRF Protection habilitado
- Senhas criptografadas
- Validação de formulários no backend
- Controle de permissões por projeto/tarefa

## 📊 Funcionalidades de ORM

### Filtros Implementados
- Filtro por status (Projetos e Tarefas)
- Filtro por prioridade (Tarefas)
- Filtro por projeto (Tarefas)
- Busca textual (título e descrição)

### Ordenação
- Por data de criação
- Por nome
- Por data limite

### Paginação
- 10 projetos por página
- 15 tarefas por página
- 20 categorias por página

### Relacionamentos
- `select_related()` para otimizar queries com ForeignKey
- `prefetch_related()` para otimizar ManyToMany
- Queries com `Q objects` para filtros complexos

## 👥 Contribuindo

Este é um projeto acadêmico desenvolvido para avaliação. Sugestões são bem-vindas!

## 📝 Licença

Projeto desenvolvido para fins educacionais - Segunda Unidade

## 👨‍💻 Autor

Desenvolvido como projeto da disciplina de Desenvolvimento Web

---

**Nota:** Este projeto atende a TODOS os requisitos obrigatórios da avaliação:
- ✅ Frontend com HTML5/CSS3 semântico e responsivo
- ✅ 100% Class-Based Views (CBVs)
- ✅ CRUD completo implementado
- ✅ PostgreSQL como banco de dados
- ✅ Autenticação e autorização completas
- ✅ 4 modelos com relacionamentos (FK, M2M, O2O)
- ✅ Filtros, ordenação e paginação com ORM
- ✅ Código limpo e bem organizado
- ✅ Interface moderna e usável
