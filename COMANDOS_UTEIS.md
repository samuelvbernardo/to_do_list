# 🔧 Comandos Úteis - TaskManager

## 🚀 Configuração Inicial

### Criar Ambiente Virtual
```powershell
python -m venv venv
```

### Ativar Ambiente Virtual
```powershell
# Windows PowerShell
.\venv\Scripts\activate

# Windows CMD
.\venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Instalar Dependências
```powershell
pip install -r requirements.txt
```

## 🗄️ PostgreSQL

### Criar Banco de Dados (psql)
```sql
CREATE DATABASE taskmanager_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE taskmanager_db TO postgres;
ALTER DATABASE taskmanager_db OWNER TO postgres;
```

### Iniciar PostgreSQL com Docker
```powershell
docker run --name postgres-taskmanager `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=taskmanager_db `
  -p 5432:5432 `
  -d postgres:15
```

### Parar/Iniciar Container Docker
```powershell
docker stop postgres-taskmanager
docker start postgres-taskmanager
```

### Conectar ao PostgreSQL
```powershell
# Via psql
psql -U postgres -d taskmanager_db

# Via Docker
docker exec -it postgres-taskmanager psql -U postgres -d taskmanager_db
```

## 🔄 Migrações Django

### Criar Migrações
```powershell
cd myproject
python manage.py makemigrations
```

### Ver SQL das Migrações
```powershell
python manage.py sqlmigrate core 0001
```

### Aplicar Migrações
```powershell
python manage.py migrate
```

### Reverter Migrações
```powershell
# Reverter para migração específica
python manage.py migrate core 0001

# Reverter todas migrações do app
python manage.py migrate core zero
```

### Limpar e Recriar Banco
```powershell
# 1. Deletar migrações antigas
Remove-Item core\migrations\*.py -Exclude "__init__.py"

# 2. Dropar e recriar banco (no PostgreSQL)
# DROP DATABASE taskmanager_db;
# CREATE DATABASE taskmanager_db;

# 3. Criar novas migrações
python manage.py makemigrations

# 4. Aplicar migrações
python manage.py migrate

# 5. Criar superusuário
python manage.py createsuperuser
```

## 👤 Gerenciamento de Usuários

### Criar Superusuário
```powershell
python manage.py createsuperuser
```

### Criar Usuário via Shell
```powershell
python manage.py shell
```
```python
from django.contrib.auth.models import User
from core.models import PerfilUsuario

user = User.objects.create_user(
    username='joao',
    email='joao@example.com',
    password='senha123',
    first_name='João',
    last_name='Silva'
)
PerfilUsuario.objects.create(user=user, cargo='Desenvolvedor')
```

### Alterar Senha
```powershell
python manage.py changepassword username
```

## 🗂️ Banco de Dados

### Acessar Shell do Django
```powershell
python manage.py shell
```

### Executar Script Python
```powershell
python manage.py shell < populate_db.py
```

### Exportar Dados (Fixture)
```powershell
# Todos os dados
python manage.py dumpdata > backup.json

# App específico
python manage.py dumpdata core > core_backup.json

# Modelo específico
python manage.py dumpdata core.Tarefa > tarefas.json
```

### Importar Dados (Fixture)
```powershell
python manage.py loaddata backup.json
```

### Flush Database (limpar dados)
```powershell
python manage.py flush
```

## 🖥️ Servidor de Desenvolvimento

### Iniciar Servidor
```powershell
python manage.py runserver
```

### Iniciar em Porta Diferente
```powershell
python manage.py runserver 8080
```

### Permitir Acesso Externo
```powershell
python manage.py runserver 0.0.0.0:8000
```

## 🧪 Testes

### Executar Todos os Testes
```powershell
python manage.py test
```

### Testar App Específico
```powershell
python manage.py test core
```

### Testar com Verbosidade
```powershell
python manage.py test --verbosity=2
```

## 📊 Inspeção e Debug

### Verificar Problemas
```powershell
python manage.py check
```

### Ver Configurações
```powershell
python manage.py diffsettings
```

### Ver SQL de um Modelo
```powershell
python manage.py sqlmigrate core 0001
```

### Shell Interativo
```powershell
python manage.py shell
```
```python
# Importar modelos
from core.models import Tarefa, Projeto, Categoria

# Listar todos
Projeto.objects.all()

# Filtrar
Tarefa.objects.filter(status='PENDENTE')

# Contar
Tarefa.objects.count()

# Criar
projeto = Projeto.objects.create(
    nome='Novo Projeto',
    responsavel_id=1,
    data_inicio='2024-01-01'
)
```

## 📁 Arquivos Estáticos

### Coletar Arquivos Estáticos
```powershell
python manage.py collectstatic
```

### Limpar Arquivos Estáticos
```powershell
python manage.py collectstatic --clear --noinput
```

## 🔧 Utilitários

### Criar Nova App Django
```powershell
python manage.py startapp nome_app
```

### Criar Superusuário Sem Interação
```powershell
python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
```

### Ver Versão do Django
```powershell
python -m django --version
```

### Listar Comandos Disponíveis
```powershell
python manage.py help
```

## 🐳 Docker (Opcional)

### Dockerfile Exemplo
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: taskmanager_db
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
  
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
```

## 📦 Gerenciamento de Pacotes

### Atualizar Requirements.txt
```powershell
pip freeze > requirements.txt
```

### Instalar Pacote Específico
```powershell
pip install nome-pacote==versao
```

### Listar Pacotes Instalados
```powershell
pip list
```

### Verificar Pacotes Desatualizados
```powershell
pip list --outdated
```

## 🔍 Debugging

### Ativar Debug Toolbar
```python
# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Ver Queries SQL
```python
from django.db import connection
print(connection.queries)
```

## 🚨 Resolução de Problemas

### Erro: "Port already in use"
```powershell
# Encontrar processo usando porta 8000
netstat -ano | findstr :8000

# Matar processo
taskkill /PID <PID> /F
```

### Erro: "No module named 'core'"
```powershell
# Verificar INSTALLED_APPS em settings.py
# Deve conter 'core'
```

### Erro: PostgreSQL connection
```powershell
# Verificar se PostgreSQL está rodando
# Verificar credenciais em settings.py
# Testar conexão:
psql -U postgres -d taskmanager_db
```

### Reset Completo
```powershell
# 1. Deletar banco
DROP DATABASE taskmanager_db;
CREATE DATABASE taskmanager_db;

# 2. Deletar migrações
Remove-Item core\migrations\*.py -Exclude "__init__.py"

# 3. Recriar tudo
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 📝 Atalhos Úteis

### Criar e Aplicar Migrações de Uma Vez
```powershell
python manage.py makemigrations; python manage.py migrate
```

### Backup Rápido do Banco
```powershell
python manage.py dumpdata > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").json
```

### Limpar Cache Python
```powershell
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse
```

## 🎯 Comandos para Apresentação

### Setup Rápido
```powershell
# Execute na ordem:
.\venv\Scripts\activate
cd myproject
python manage.py migrate
python manage.py shell < populate_db.py
python manage.py runserver
```

### Criar Usuário de Teste Rápido
```python
# No Django shell
from django.contrib.auth.models import User
from core.models import PerfilUsuario

u = User.objects.create_user('demo', 'demo@demo.com', 'demo123')
u.first_name = 'Demo'
u.last_name = 'User'
u.save()
PerfilUsuario.objects.create(user=u)
```

---

## 📚 Referências Rápidas

- **Django Docs:** https://docs.djangoproject.com/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/
- **Bootstrap Docs:** https://getbootstrap.com/docs/
- **Django Admin:** http://localhost:8000/admin/
- **Aplicação:** http://localhost:8000/

---

**Dica:** Mantenha este arquivo aberto durante o desenvolvimento para acesso rápido aos comandos!
