# Add these at the top of your settings.py
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# pip install psycopg2
import psycopg2

# Parâmetros de conexão com o banco de dados PostgreSQL
dbname = 'elitefc'
user = 'elitefc_owner'
password = 'JZmq8x7rPHMf'
host = 'ep-fancy-salad-a5y97w8t.us-east-2.aws.neon.tech'
port = '5432'  # Porta padrão do PostgreSQL

# Tentativa de conexão
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Conexão estabelecida com sucesso!")
    
    # Aqui você pode executar consultas, inserções, etc. Exemplo:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogador")
    rows = cursor.fetchall() # leitura saida da query
    rows = cursor.commit() # gravar da query

    for row in rows:
        print(row)
    cursor.close()
    conn.close()
    

except psycopg2.Error as e:
    print("Erro ao conectar ao PostgreSQL:", e)