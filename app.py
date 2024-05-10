# Add these at the top of your settings.py
from os import getenv
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from random import shuffle
# pip install python-dotenv psycopg2 Flask

# ******************************************* MAIN ********************************************
# ******************************************* MAIN ********************************************
load_dotenv()

# Parâmetros de conexão com o banco de dados PostgreSQL
dbname = getenv('PGDATABASE')
user = getenv('PGUSER')
password = getenv('PGPASSWORD')
host = getenv('PGHOST')
port = getenv('PGPORT')

senha_correta = "123" # 

# # ****************************** ROTAS PRONTAS **************************************
app = Flask(__name__)

def carregar_jogadores():
    try:
        conexao = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Conexão estabelecida com sucesso AO BANCO DE DADOS!")
        
        cursor = conexao.cursor()
        # *********************** VISUALIZAR TABELA ATUAL *********************
        comando3 = 'SELECT * FROM jogador;'
        cursor.execute(comando3)
        jogadores = cursor.fetchall() #ler
        # Transforma os resultados em uma lista de dicionários
        resultado = []
        for jogador in jogadores:
            jogador_dict = {
                'id': jogador[0],  # supondo que o primeiro campo seja o ID
                'nome': jogador[1],  # supondo que o segundo campo seja o nome
                'posicao': jogador[2],  # supondo que o segundo campo seja o nome
                'nivel': jogador[3],  # supondo que o segundo campo seja o nome
                'status': jogador[4],  # supondo que o segundo campo seja o nome
                # Adicione os outros campos conforme necessário
            }
            resultado.append(jogador_dict)

        cursor.close() # fecha cursor
        conexao.close() # fecha conexão

        return resultado
        
    except psycopg2.Error as e:
        print("Erro ao conectar ao BANCO DE DADOS:", e)

##########################################################################################################################
# *************************************************************** INDEX **************************************************
@app.route('/', methods=['GET', 'POST'])
def index():
    carregar_jogadores

    jogadores = carregar_jogadores()
    aviso = request.args.get('aviso')  # Obtém o aviso da URL, se houver
    return render_template('index.html', jogadores=jogadores, aviso=aviso)

# ********************************************************** **INSERT JOGADOR ***********************************************
@app.route('/adicionar_jogador', methods=['POST'])
def adicionar_jogador():
    if request.method == 'POST':
        nomeRecebido = request.form['nome']
        nome = nomeRecebido.strip().capitalize()
        posicao = request.form['posicao']
        nivel = request.form['nivel']
        status = "Pendente"
        print(f'nome adicionado ..... ',nomeRecebido)
        print(f'nome adicionado ..... ',nome)
        # Tentativa de conexão
        try:
            conexao = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Conexão estabelecida com sucesso AO BANCO DE DADOS!")

            cursor = conexao.cursor()
            comando = f'INSERT INTO jogador(nomeJogador, posicao, nivel, status) VALUES (\'{nome}\', \'{posicao}\', \'{nivel}\', \'{status}\')'
            cursor.execute(comando)
            conexao.commit() # editar

            cursor.close()
            conexao.close()

        except psycopg2.Error as e:
            print("Erro ao conectar ao BANCO DE DADOS:", e)

    # Após adicionar o jogador, redirecione para a página inicial ou para onde desejar
    return redirect(url_for('index'))

# ********************************************************** EXCLUIR JOGADOR ***********************************************
@app.route('/excluir_jogador', methods=['POST'])
def excluir_jogador():
    
    if request.method == 'POST':
        # Obter o nome do jogador do formulário
        nome_jogador = request.form['nome']
        senha_digitada = request.form.get('senha')

        print(nome_jogador , senha_digitada, senha_correta)
    
        if senha_digitada == senha_correta:

            # Tentativa de conexão
            try:
                # Conectar ao banco de dados
                conexao = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                print("Conexão estabelecida com sucesso AO BANCO DE DADOS!")

                # Criar um cursor para executar comandos SQL
                cursor = conexao.cursor()

                # Usar parâmetros preparados para evitar injeção de SQL
                comando = 'DELETE FROM jogador WHERE nomejogador = %s'
                cursor.execute(comando, (nome_jogador,))

                # Confirmar a transação
                conexao.commit()

                # Fechar o cursor e a conexão
                cursor.close()
                conexao.close()

            except psycopg2.Error as e:
                print("Erro ao conectar ao BANCO DE DADOS:", e)

    # Após excluir o jogador, redirecionar para a página inicial ou para onde desejar
    return redirect(url_for('index'))


# ************************************************************* MUDAR STATUS ****************************************************
@app.route('/mudar_status/<nome>', methods=['POST'])
def mudar_status(nome):
    if request.method == 'POST':
        novo_status = request.form.get('novo_status')

        # Tentativa de conexão
        try:
            conexao = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Conexão estabelecida com sucesso AO BANCO DE DADOS!")

            cursor = conexao.cursor()

            comando = f'UPDATE jogador SET status = \'{novo_status}\' WHERE nomeJogador = \'{nome}\''
            cursor.execute(comando)
            conexao.commit()

            cursor.close()
            conexao.close()

        except psycopg2.Error as e:
            print("Erro ao conectar ao BANCO DE DADOS:", e)

    return redirect(url_for('index'))

# # *********************************************** RESETAR STATUS **************************************************************
# senha_correta = "123" # Defina a senha correta

@app.route('/resetar', methods=['POST'])
def resetar_status():
    senha_digitada = request.form.get('senha')
    print(f'senha digitada.......', senha_digitada)
    print(f'senha correta.......', senha_correta)

    if senha_digitada == senha_correta:
        # Tentativa de conexão
        try:
            conexao = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            cursor = conexao.cursor()

            # Use instrução parametrizada
            comando = 'UPDATE jogador SET status = %s'
            cursor.execute(comando, ('Pendente',))  # Use uma tupla para os parâmetros

            conexao.commit()

            cursor.close()  # fecha cursor
            conexao.close()  # fecha conexão

            return redirect(url_for('index'))

        except psycopg2.Error as e:
            print("Erro ao conectar ao BANCO DE DADOS:", e)

            # Se ocorrer um erro, você pode querer redirecionar para uma página de erro
            return redirect(url_for('erro'))

    else:
        # Senha incorreta, redirecionar de volta à página index
        return redirect(url_for('index'))



@app.route('/sortear', methods=['POST'])
def sortear():
    times_sorteados, mensagem_erro = realizar_sorteio()     # Chama a função realizar_sorteio()

    # Adicione os prints para depuração
    if times_sorteados:
    #   print("Time 1:", times_sorteados["time1"])
    #   print("Time 2:", times_sorteados["time2"])
    #   print("Somatório Níveis Time 1:",
    #         times_sorteados["somatorio_niveis_time1"])
    #   print("Somatório Níveis Time 2:",
    #         times_sorteados["somatorio_niveis_time2"])
      return render_template('resultado.html', resultado_sorteio=times_sorteados)
    else:
      # print("Erro no sorteio:", mensagem_erro)
      return render_template('erro_sorteio.html', mensagem_erro=mensagem_erro)

def realizar_sorteio():
    jogadores = carregar_jogadores()

    # Tentativa de conexão
    try:
        conexao = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        # Criar um cursor
        cursor = conexao.cursor()

        # Consulta para selecionar todas as informações da coluna "status"
        comando = "SELECT status FROM jogador"

        # Executar a consulta
        cursor.execute(comando)

        # Obter todos os resultados
        resultados = cursor.fetchall()

        # Verificar se há algum status "pendente"
        pendente = False
        for status in resultados:
            if status[0] == 'Pendente':
                pendente = True
                break

        # Fechar cursor e conexão
        cursor.close()
        conexao.close()

        # Se houver algum status pendente, faça algo
        if pendente:
            print("Há jogadores com status pendente.")
            mensagem = "Aguarde até que todos os jogadores confirmem o status."
            return None, mensagem

        else:
            # Filtrar jogadores que estão dentro
            jogadores_dentro = [
                jogador for jogador in jogadores if jogador['status'] == 'Dentro'
            ]

            # Ordenar jogadores por posição desejada
            posicoes_desejadas = ['Goleiro', 'Zagueiro', 'Meia', 'Atacante']
            jogadores_dentro.sort(
                key=lambda x: (posicoes_desejadas.index(x['posicao']), x['nivel']))

            # Dividir jogadores por  posição primeiro e depois nivel
            jogadores_dentro.sort(key=lambda x: (x['posicao'], x['nivel']))

            # # Dividir jogadores em dois times, garantindo equilíbrio nas notas e posições
            # time1 = jogadores_dentro[::2]
            # time2 = jogadores_dentro[1::2]

            # Crie duas listas com os índices dos jogadores, para garantir que os times tenham tamanhos iguais
            indices_time1 = list(range(0, len(jogadores_dentro), 2))
            indices_time2 = list(range(1, len(jogadores_dentro), 2))

            # Embaralhe os índices para garantir que os jogadores sejam sorteados aleatoriamente
            shuffle(indices_time1)
            shuffle(indices_time2)

            # Monte os times com base nos índices sorteados
            time1 = [jogadores_dentro[i] for i in indices_time1]
            time2 = [jogadores_dentro[i] for i in indices_time2]



            # Calcular somatório dos níveis para cada time
            somatorio_niveis_time1 = sum(jogador['nivel'] for jogador in time1)
            somatorio_niveis_time2 = sum(jogador['nivel'] for jogador in time2)

            # Calcular somatório dos níveis para cada setor do Time 1
            soma_niveis_goleiros_zagueiros_time1 = sum(jogador['nivel'] for jogador in time1 if jogador['posicao'] in ('Goleiro', 'Zagueiro'))
            soma_niveis_meias_time1 = sum(jogador['nivel'] for jogador in time1 if jogador['posicao'] == 'Meia')
            soma_niveis_atacantes_time1 = sum(jogador['nivel'] for jogador in time1 if jogador['posicao'] == 'Atacante')

            # Calcular somatório total dos níveis para o Time 1
            somatorio_niveis_time1 = soma_niveis_goleiros_zagueiros_time1 + soma_niveis_meias_time1 + soma_niveis_atacantes_time1

            # Cálculos de porcentagem para o Time 1
            porcentagem_goleiros_zagueiros_time1 = round((soma_niveis_goleiros_zagueiros_time1 / somatorio_niveis_time1) * 100)
            porcentagem_meia_time1 = round((soma_niveis_meias_time1 / somatorio_niveis_time1) * 100)
            porcentagem_atacante_time1 = round((soma_niveis_atacantes_time1 / somatorio_niveis_time1) * 100)


            # print(soma_niveis_goleiros_zagueiros_time1)
            # print(soma_niveis_meias_time1)
            # print(soma_niveis_atacantes_time1)

            # print(porcentagem_goleiros_zagueiros_time1)
            # print(porcentagem_meia_time1)
            # print(porcentagem_atacante_time1)

            # Calcular somatório dos níveis para cada setor do Time 2
            soma_niveis_goleiros_zagueiros_time2 = sum(jogador['nivel'] for jogador in time2 if jogador['posicao'] in ('Goleiro', 'Zagueiro'))
            soma_niveis_meias_time2 = sum(jogador['nivel'] for jogador in time2 if jogador['posicao'] == 'Meia')
            soma_niveis_atacantes_time2 = sum(jogador['nivel'] for jogador in time2 if jogador['posicao'] == 'Atacante')

            # Calcular somatório total dos níveis para o Time 2
            somatorio_niveis_time2 = soma_niveis_goleiros_zagueiros_time2 + soma_niveis_meias_time2 + soma_niveis_atacantes_time2

            # Cálculos de porcentagem para o Time 2
            porcentagem_goleiros_zagueiros_time2 = round((soma_niveis_goleiros_zagueiros_time2 / somatorio_niveis_time2) * 100)
            porcentagem_meia_time2 = round((soma_niveis_meias_time2 / somatorio_niveis_time2) * 100)
            porcentagem_atacante_time2 = round((soma_niveis_atacantes_time2 / somatorio_niveis_time2) * 100)

            # print(soma_niveis_goleiros_zagueiros_time2)
            # print(soma_niveis_meias_time2)
            # print(soma_niveis_atacantes_time2)

            # print(porcentagem_goleiros_zagueiros_time2)
            # print(porcentagem_meia_time2)
            # print(porcentagem_atacante_time2)


            times_sorteados = {
            "time1": time1,
            "time2": time2,
            "somatorio_niveis_time1": somatorio_niveis_time1,
            "somatorio_niveis_time2": somatorio_niveis_time2,
            "porcentagem_goleiros_zagueiros_time1": porcentagem_goleiros_zagueiros_time1,
            "porcentagem_meia_time1": porcentagem_meia_time1,
            "porcentagem_atacante_time1": porcentagem_atacante_time1,
            "porcentagem_goleiros_zagueiros_time2": porcentagem_goleiros_zagueiros_time2,
            "porcentagem_meia_time2": porcentagem_meia_time2,
            "porcentagem_atacante_time2": porcentagem_atacante_time2
            }
    except psycopg2.Error as e:
        print("Erro ao conectar ao BANCO DE DADOS:", e)

    return times_sorteados, None


if __name__ == '__main__':
    # # Ativa o modo de depuração para reiniciar automaticamente o servidor em caso de alterações no código
    # port = int(os.getenv('PORT', 10000))  # Use a porta definida pela variável de ambiente PORT, ou 9090 se não estiver definida
    app.run(host='0.0.0.0', port=9090)