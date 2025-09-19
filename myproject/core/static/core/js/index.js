let tarefas = JSON.parse(localStorage.getItem('tarefas')) || [];

if (tarefas.length === 0) {
    const backendTarefas = JSON.parse(document.getElementById('tarefas-data').textContent);
    tarefas = backendTarefas.map(t => ({ titulo: t.fields.titulo }));
    localStorage.setItem('tarefas', JSON.stringify(tarefas));
}

if (tarefas.length > 0) {
    const letreiro = document.getElementById('letreiro-tarefas');
    const span = document.createElement('span');
    span.textContent = tarefas.map(t => t.titulo).join(' | ');
    span.style.whiteSpace = 'nowrap';
    span.style.position = 'absolute';
    span.style.left = letreiro.offsetWidth + 'px';
    letreiro.appendChild(span);

    const velocidade = 2;

    function animar() {
        const posAtual = parseFloat(span.style.left);
        span.style.left = (posAtual - velocidade) + 'px';
        if (posAtual + span.offsetWidth < 0) {
            span.style.left = letreiro.offsetWidth + 'px';
        }
        requestAnimationFrame(animar);
    }
    animar();
}

