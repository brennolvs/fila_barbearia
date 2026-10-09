# Fila de Barbearia

Aplicação web em Python com Flask para gerenciar a fila de atendimento de uma barbearia. O cliente entra numa fila virtual informando nome, telefone (opcional) e o serviço desejado. O barbeiro tem uma área protegida por senha para chamar o próximo cliente.

## Funcionalidades

### Visão do cliente

- Ver a fila de espera e o cliente que está sendo atendido no momento
- Entrar na fila informando nome, telefone e serviço
- Receber a confirmação da posição na fila

### Visão do barbeiro (área logada)

- Login com senha
- Chamar o próximo cliente, que sai da fila e fica em destaque
- Ver o telefone dos clientes, que fica oculto para quem não está logado
- Atualizar a fila e fazer logout

## Tecnologias

- Python 3
- Flask
- Jinja2 (templates HTML)
- HTML5 e CSS3
- Gunicorn (servidor de produção)

## Arquitetura

Toda a regra de negócio fica no back-end (`app.py`). Os templates apenas exibem os dados prontos que o servidor entrega:

- A lista de serviços é definida no back-end, e o servidor só aceita os serviços dessa lista.
- Os dados do cliente são validados no servidor: nome obrigatório, limites de tamanho e serviço válido.
- O texto de cada cliente, sua posição na fila e a regra de exibir o telefone apenas para o barbeiro são resolvidos no servidor.
- As rotas do barbeiro são protegidas no servidor. Não basta esconder o botão na tela.
- Depois de cada ação, o servidor redireciona e exibe uma mensagem de retorno (padrão Post/Redirect/Get). Assim, atualizar a página não repete a ação.

## Rotas

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| GET | `/` | Exibe a fila e o cliente atual | Público |
| POST | `/adicionar` | Adiciona um cliente à fila | Público |
| POST | `/chamar` | Chama o próximo cliente | Barbeiro |
| POST | `/atualizar_fila` | Recarrega a fila | Barbeiro |
| GET/POST | `/login` | Login do barbeiro | Público |
| GET | `/logout` | Encerra a sessão do barbeiro | Público |

## Estrutura do projeto

```
fila_barbearia/
├── app.py              # Rotas, validações e regras da fila
├── templates/
│   ├── index.html      # Tela da fila
│   └── login.html      # Tela de login do barbeiro
├── requirements.txt    # Dependências
└── Procfile            # Comando de inicialização para deploy
```

## Como executar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/brennolvs/fila_barbearia.git
   cd fila_barbearia
   ```
2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python app.py
   ```
5. Acesse `http://localhost:5000`.

## Variáveis de ambiente

| Variável | Descrição | Valor padrão (apenas para desenvolvimento) |
|---|---|---|
| `SENHA_BARBEIRO` | Senha de acesso do barbeiro | `barbeiro123` |
| `SECRET_KEY` | Chave usada para assinar a sessão | `chave-de-desenvolvimento` |
| `PORT` | Porta do servidor | `5000` |

Em produção, defina sempre `SENHA_BARBEIRO` e `SECRET_KEY` com valores próprios.

## Deploy

O `Procfile` inicia a aplicação com o Gunicorn (`web: gunicorn app:app`), o que permite publicá-la em plataformas como Render, Railway ou Heroku.

## Limitações conhecidas

- A fila fica em memória, então é perdida quando o servidor reinicia.
- Pelo mesmo motivo, a aplicação deve rodar com um único worker do Gunicorn. Com vários workers, cada um teria a sua própria fila.

## Possíveis melhorias

- Guardar a fila em um banco de dados (por exemplo, SQLite)
- Atualizar a fila automaticamente na tela, sem precisar recarregar
- Adicionar testes automatizados das rotas com pytest
- Mover o CSS para arquivos estáticos

## Autor

**Brenno Alves**  
[LinkedIn](https://linkedin.com/in/brennolvs) · [GitHub](https://github.com/brennolvs)
