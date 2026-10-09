import hmac
import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-de-desenvolvimento')

# Senha do barbeiro: definida por variável de ambiente em produção
SENHA_BARBEIRO = os.environ.get('SENHA_BARBEIRO', 'barbeiro123')

# Serviços oferecidos. O formulário é montado a partir desta lista e
# o back-end só aceita valores que estejam nela.
SERVICOS = [
    'Corte Simples',
    'Corte + Pigmentação',
    'Corte + Barba',
    'Corte + Barba + Pigmentação',
    'Barba',
    'Platinado',
    'Sobrancelha',
    'Pézinho',
]

TAMANHO_MAXIMO_NOME = 60
TAMANHO_MAXIMO_TELEFONE = 20

# Estado da fila (em memória: é perdido quando o servidor reinicia)
fila = []
cliente_atual = None


def is_barber():
    return session.get('is_barber', False)


def somente_barbeiro(rota):
    """Bloqueia a rota para quem não está logado como barbeiro."""
    @wraps(rota)
    def wrapper(*args, **kwargs):
        if not is_barber():
            flash('Acesso permitido apenas para o barbeiro.', 'erro')
            return redirect(url_for('login'))
        return rota(*args, **kwargs)
    return wrapper


def formatar_cliente(cliente, mostrar_telefone):
    """Monta o texto de exibição do cliente. O telefone só aparece para o barbeiro."""
    texto = cliente['nome']
    if mostrar_telefone and cliente['telefone']:
        texto += f" - {cliente['telefone']}"
    return f"{texto} ({cliente['servico']})"


def validar_cliente(nome, telefone, servico):
    """Retorna a mensagem de erro, ou None se os dados forem válidos."""
    if not nome:
        return 'Informe o nome do cliente.'
    if len(nome) > TAMANHO_MAXIMO_NOME:
        return f'O nome deve ter no máximo {TAMANHO_MAXIMO_NOME} caracteres.'
    if len(telefone) > TAMANHO_MAXIMO_TELEFONE:
        return f'O telefone deve ter no máximo {TAMANHO_MAXIMO_TELEFONE} caracteres.'
    if servico not in SERVICOS:
        return 'Selecione um serviço válido.'
    return None


# Rota principal para exibir a fila
@app.route('/')
def index():
    barbeiro = is_barber()
    fila_exibicao = [
        {'posicao': posicao, 'texto': formatar_cliente(cliente, barbeiro)}
        for posicao, cliente in enumerate(fila, start=1)
    ]
    atual = formatar_cliente(cliente_atual, barbeiro) if cliente_atual else None
    return render_template(
        'index.html',
        fila=fila_exibicao,
        cliente_atual=atual,
        servicos=SERVICOS,
        is_barber=barbeiro,
    )


# Rota para adicionar cliente à fila
@app.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form.get('nome', '').strip()
    telefone = request.form.get('telefone', '').strip()
    servico = request.form.get('servico', '').strip()

    erro = validar_cliente(nome, telefone, servico)
    if erro:
        flash(erro, 'erro')
    else:
        fila.append({'nome': nome, 'telefone': telefone, 'servico': servico})
        flash(f'{nome} entrou na fila na posição {len(fila)}.', 'sucesso')
    return redirect(url_for('index'))


# Rota para chamar o próximo cliente (somente barbeiro)
@app.route('/chamar', methods=['POST'])
@somente_barbeiro
def chamar_cliente():
    global cliente_atual
    if fila:
        cliente_atual = fila.pop(0)
        flash(f"Cliente {cliente_atual['nome']} chamado!", 'sucesso')
    else:
        cliente_atual = None
        flash('Não há clientes na fila.', 'aviso')
    return redirect(url_for('index'))


@app.route('/atualizar_fila', methods=['POST'])
@somente_barbeiro
def atualizar_fila():
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha', '')
        if hmac.compare_digest(senha.encode(), SENHA_BARBEIRO.encode()):
            session['is_barber'] = True
            return redirect(url_for('index'))
        flash('Senha incorreta. Tente novamente.', 'erro')
        return redirect(url_for('login'))
    return render_template('login.html')


# Rota para logout do barbeiro
@app.route('/logout')
def logout():
    session.pop('is_barber', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
