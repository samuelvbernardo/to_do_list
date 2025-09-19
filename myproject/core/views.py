from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa
from django.core.serializers import serialize
from .forms import TarefaForm

def lista_tarefas(request):
    filtro = request.GET.get('filtro')
    tarefas = Tarefa.objects.all()
    
    if filtro == 'pendentes':
        tarefas = tarefas.filter(status='PENDENTE')
    elif filtro == 'concluidas':
        tarefas = tarefas.filter(status='CONCLUIDA')
    
    # Serializa apenas o campo 'titulo' para o JS
    tarefas_json = serialize('json', tarefas, fields=('titulo',))
    
    return render(request, 'core/lista_tarefas.html', {
        'tarefas': tarefas,
        'tarefas_json': tarefas_json
    })

def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()
    return render(request, 'core/criar_tarefa.html', {'form': form})

def editar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'core/editar_tarefa.html', {'form': form})

def excluir_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == 'POST':
        tarefa.delete()
        return redirect('lista_tarefas')
    return render(request, 'core/excluir_tarefa.html', {'object': tarefa})
