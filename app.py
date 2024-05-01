# Add these at the top of your settings.py
from os import getenv
from dotenv import load_dotenv
import psycopg2
# pip install psycopg2 dotenv
# ******************************************* DEVELOP ********************************************
# ******************************************* DEVELOP ********************************************
load_dotenv()

# Parâmetros de conexão com o banco de dados PostgreSQL
dbname = getenv('PGDATABASE')
user = getenv('PGUSER')
password = getenv('PGPASSWORD')
host = getenv('PGHOST')
port = getenv('PGPORT')

# Tentativa de conexão
try:
    conexao = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Conexão estabelecida com sucesso!")
    
    # Aqui você pode executar consultas, inserções, etc. Exemplo:
    cursor = conexao.cursor()

    # # *********************** VISUALIZAR TABELA ATUAL *********************
    # comando = 'SELECT * FROM jogador;'
    # cursor.execute(comando)
    # resultado = cursor.fetchall() #ler
    # for i in resultado:
    #     print(i)
    # print("*"*30)

    # ********************** INSERT JOGADOR ******************************
    nomeJogador = 'Tiago'
    posicao = 'Atacante'
    nivel = 8
    status = 'Pendente'
    comando = 'INSERT INTO jogador(nomeJogador, posicao, nivel, status) VALUES (%s, %s, %s,%s)'
    valores = (nomeJogador, posicao, nivel, status)
    cursor.execute(comando, valores)
    conexao.commit()

    cursor.close()
    conexao.close()
    
except psycopg2.Error as e:
    print("Erro ao conectar ao PostgreSQL:", e)




# # ********************** INSERT JOGADOR ******************************
# nomeJogador = 'Joao'
# posicao = "Atacante"
# nivel = 8
# comando = f'INSERT INTO jogador(nomeJogador, posicao, nivel) VALUES ("{nomeJogador}", "{posicao}", "{nivel}")'
# cursor.execute(comando)
# conexao.commit() # editar

# # ********************** DELETE JOGADOR *******************************
# nomeJogador = "Dato"
# comando = f'DELETE FROM jogador WHERE nomeJogador = "{nomeJogador}"'
# cursor.execute(comando)
# conexao.commit()

# *********************** UPDATE JOGADOR ***********************************
# nomeJogador = "Joao"
# nivel = 10
# status = "Pendente"
# comando = f'UPDATE jogador SET status = "{status}" WHERE nomeJogador = "{nomeJogador}"'
# cursor.execute(comando)
# conexao.commit()