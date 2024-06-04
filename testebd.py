import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        # Formato da URL de conexão:
        # postgresql://usuario:senha@host:porta/nome_do_banco
        connection_url = (
            "postgres://root:aYc0oP9i6HDTvrhHPcGs3xobfkgV7IVK@dpg-cp7tpcsf7o1s73el4h40-a/database_elitefc"
        )
        
        # Conectando ao banco de dados usando a URL
        connection = psycopg2.connect(connection_url)
        print("Conexão com o banco de dados bem-sucedida")
        return connection
    except OperationalError as e:
        print(f"Erro ao conectar ao BANCO DE DADOS: {e}")
        return None

# Testando a conexão
conn = create_connection()
if conn:
    # Fechar a conexão se for bem-sucedida
    conn.close()
