# Sortear times equilibrado - dato®

## Introdução:
Este projeto tem como objetivo criar uma aplicação web para gerenciar jogadores de futebol. Utilizando `Flask` como framework web e `PostgreSQL como banco de dados`, a aplicação permite adicionar, atualizar, excluir e sortear jogadores em times equilibrados. A autenticação de sessão e a manipulação de variáveis de ambiente são realizadas com a biblioteca dotenv.

## Funcionalidades:
Adicionar Jogador: Permite adicionar novos jogadores ao banco de dados.
Atualizar Jogador: Permite atualizar a posição e o nível dos jogadores existentes.
Excluir Jogador: Permite excluir jogadores do banco de dados.
Mudar Status: Permite alterar o status dos jogadores (Pendente, Dentro, etc.).
Sortear Times: Realiza o sorteio de jogadores em dois times equilibrados.
Reset de Status: Reseta para a próxima partida, o status de todos os jogadores para "Pendente"

### Tecnologia: 🎯 Postgree, psycopg2, dotenv, Render(hospedagem), Python, CI/CD, Flask, Html, CSS

![image](https://github.com/datocarneiro/Sortear_times/assets/132966071/2e2218dd-6f6c-4818-800d-992f2dcc6c3e)


## Documentação

### Instalação e Configuração
Instale as Dependências:
`pip install -r requirements.txt`

### Configuração do Banco de Dados:
Crie um banco de dados PostgreSQL e configure as credenciais.
Crie a tabela jogador com a seguinte estrutura:
```sql
CREATE TABLE jogador (
  id SERIAL PRIMARY KEY,
  nomeJogador VARCHAR(100),
  posicao VARCHAR(50),
  nivel INTEGER,
  status VARCHAR(50)
);
```

### Configure o Arquivo .env:
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
```env
PGDATABASE=<nome_do_banco_de_dados>
PGUSER=<usuario_do_banco>
PGPASSWORD=<senha_do_banco>
PGHOST=<host_do_banco>
PGPORT=<porta_do_banco>
```
### Rotas
Rota Principal:
URL: /
Métodos: GET, POST
Descrição: Exibe a lista de jogadores e permite operações de gerenciamento.
Adicionar Jogador:

URL: /adicionar_jogador
Métodos: POST
Parâmetros:
nome: Nome do jogador.
posicao: Posição desejada.
nivel: Nível de habilidade.
Descrição: Adiciona um novo jogador ao banco de dados.
Atualizar Jogador:

URL: /atualizar_jogador
Métodos: POST
Parâmetros:
nomeAtualizar: Nome do jogador a ser atualizado.
nova_posicao: Nova posição desejada.
novo_nivel: Novo nível de habilidade.
senhaatualizar: Senha para autenticação.
Descrição: Atualiza as informações do jogador.
Excluir Jogador:

URL: /excluir_jogador
Métodos: POST
Parâmetros:
nome: Nome do jogador a ser excluído.
senha: Senha para autenticação.
Descrição: Remove um jogador do banco de dados.
Mudar Status:

URL: /mudar_status/<nome>
Métodos: POST
Parâmetros:
novo_status: Novo status do jogador.
Descrição: Altera o status do jogador especificado.
Resetar Status:

URL: /resetar
Métodos: POST
Parâmetros:
senha: Senha para autenticação.
Descrição: Reseta o status de todos os jogadores para "Pendente".
Sortear Times:

URL: /sortear
Métodos: POST
Descrição: Realiza o sorteio de times equilibrados entre os jogadores com status "Dentro".
