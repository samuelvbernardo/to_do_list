from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Projetos
    path('projetos/', views.ProjetoListView.as_view(), name='projeto_list'),
    path('projetos/<int:pk>/', views.ProjetoDetailView.as_view(), name='projeto_detail'),
    path('projetos/novo/', views.ProjetoCreateView.as_view(), name='projeto_create'),
    path('projetos/<int:pk>/editar/', views.ProjetoUpdateView.as_view(), name='projeto_update'),
    path('projetos/<int:pk>/excluir/', views.ProjetoDeleteView.as_view(), name='projeto_delete'),
    
    # Tarefas
    path('tarefas/', views.TarefaListView.as_view(), name='tarefa_list'),
    path('tarefas/<int:pk>/', views.TarefaDetailView.as_view(), name='tarefa_detail'),
    path('tarefas/nova/', views.TarefaCreateView.as_view(), name='tarefa_create'),
    path('tarefas/<int:pk>/editar/', views.TarefaUpdateView.as_view(), name='tarefa_update'),
    path('tarefas/<int:pk>/excluir/', views.TarefaDeleteView.as_view(), name='tarefa_delete'),
    
    # Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    
    # Perfil
    path('perfil/', views.PerfilUsuarioUpdateView.as_view(), name='perfil_update'),
]
