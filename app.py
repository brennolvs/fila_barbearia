from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key_for_session_management'

# Lista para armazenar os clientes na fila
fila = []
cliente_atual = None  # Variável global para armazenar o cliente em destaque

# Rota principal para exibir a fila
@app.route('/')
def index():
    global cliente_atual  # Acessando a variável global
    is_barber = session.get('is_barber', False)
    return render_template('index.html', fila=fila, cliente_atual=cliente_atual, is_barber=is_barber)

# Rota para adicionar cliente à fila
@app.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')  # Pode ser vazio
    servico = request.form.get('servico')

    # Verificando se o nome e o serviço estão preenchidos
    if nome and servico:
        # Se telefone não for preenchido, armazene como uma string vazia
        telefone = telefone if telefone else ''
        fila.append({"nome": nome, "telefone": telefone, "servico": servico})
    return redirect(url_for('index'))

# Rota para chamar o próximo cliente (somente barbeiro)
@app.route('/chamar', methods=['POST'])
def chamar_cliente():
    global cliente_atual  # Acessando a variável global
    # Verifique se há clientes na fila
    if fila:
        cliente_atual = fila.pop(0)  # Pega o primeiro cliente da fila
        mensagem = f"Cliente {cliente_atual['nome']} chamado!"
    else:
        cliente_atual = None  # Caso não haja clientes, defina como None
        mensagem = "Não há clientes na fila."
    
    # Passando cliente_atual para o template, mesmo que seja None
    return render_template('index.html', fila=fila, cliente_atual=cliente_atual, mensagem=mensagem, is_barber=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == 'barbeiro123':  # Senha fixa para o barbeiro
            session['is_barber'] = True
            return redirect(url_for('index'))
        else:
            # Mensagem de senha incorreta
            mensagem = "Senha incorreta. Tente novamente."
            return render_template('login.html', mensagem=mensagem)
    return render_template('login.html')

# Rota para logout do barbeiro
@app.route('/logout')
def logout():
    session.pop('is_barber', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port)
