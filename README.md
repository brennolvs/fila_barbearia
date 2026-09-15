# 💈 Fila de Barbearia - Flask App

Este é um mini projeto de gerenciamento de fila para barbearias desenvolvido em Python com o framework Flask. A aplicação permite que clientes entrem em uma fila virtual informando nome, telefone e o serviço desejado. O barbeiro possui uma área restrita (autenticada por senha) para chamar o próximo cliente da fila e gerenciar os atendimentos.

## 🚀 Funcionalidades

### 👤 Visão do Cliente
*   Visualizar a fila de espera em tempo real.
*   Ver quem é o cliente que está sendo atendido no momento.
*   Preencher um formulário simples para entrar na fila (Nome, Telefone e Serviço).

### ✂️ Visão do Barbeiro (Área Logada)
*   Sistema de login com senha fixa (`barbeiro123`).
*   Botão exclusivo para chamar o próximo cliente (remove o primeiro da fila e o coloca em destaque).
*   Visualização de informações completas de contato dos clientes na fila.
*   Opção de logout para encerrar a sessão de gerenciamento.

## 🛠️ Tecnologias Utilizadas

*   **Python 3**
*   **Flask** (Framework Web)
*   **HTML5 / CSS3** (Interface do usuário através de templates Jinja2)

## 📦 Como Instalar e Executar o Projeto

Siga os passos abaixo para rodar a aplicação na sua máquina local:

### 1. Clonar o Repositório
```bash
git clone https://github.com
cd seu-repositorio
```

### 2. Configurar o Ambiente Virtual (Opcional, mas recomendado)
```bash
# No Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# No Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as Dependências
Como o projeto utiliza o Flask, você pode instalá-lo diretamente via pip:
```bash
pip install Flask
```

### 4. Executar a Aplicação
Execute o arquivo principal do projeto:
```bash
python app.py
```

A aplicação estará disponível no seu navegador através do endereço: `http://localhost:5000`

## 🔒 Credenciais de Acesso (Barbeiro)

Para acessar o painel de gerenciamento do barbeiro e simular o atendimento:
*   **Senha:** `barbeiro123`

## 📝 Notas de Implementação

*   **Persistência de dados:** Atualmente, a fila é armazenada em memória (`list` do Python). Isso significa que, se o servidor for reiniciado, a fila será resetada.
*   **Deploy:** O código já está configurado para ler a porta a partir das variáveis de ambiente (`os.environ.get('PORT')`), facilitando o deploy em plataformas como Render ou Railway.
