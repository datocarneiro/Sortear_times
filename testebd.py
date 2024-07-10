import psycopg2
from psycopg2 import OperationalError

# Dados de conexão com o banco de dados
dbname = "elitefc"
user = "dato"
password = "1234"
host = "localhost"

# Comando SQL para criar a tabela
create_table_query = '''
CREATE SCHEMA IF NOT EXISTS elitefc;

CREATE TABLE elitefc.jogador(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    posicao VARCHAR(50) NOT NULL,
    nivel INTEGER CHECK (nivel BETWEEN 1 AND 10) NOT NULL,
    status BOOLEAN DEFAULT TRUE
);
'''
connection = None

try:
    # Conectar ao banco de dados
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = connection.cursor()
    
    # Executar o comando SQL para criar a tabela
    cursor.execute(create_table_query)
    
    # Commit para salvar as alterações
    connection.commit()
    
    print("Tabela 'jogador' criada com sucesso!")

except OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

finally:
    # Fechar a conexão
    if connection:
        cursor.close()
        connection.close()
