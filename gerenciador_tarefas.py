import pyodbc
import sys
import time

# --- PASSO 1: CONFIGURE A CONEXÃO AQUI ---
# IMPORTANTE:
# 1. Tenha o "MySQL ODBC Driver" instalado no seu computador.
# 2. O nome do DRIVER deve ser exatamente igual ao instalado.
#    - No Windows, procure "Fontes de Dados ODBC" e veja a aba "Drivers".
#    - Exemplo comum: "MySQL ODBC 8.0 Unicode Driver"
CONNECTION_STRING = (
    "DRIVER={MySQL ODBC 9.4 Unicode Driver};"
    "SERVER=localhost;"
    "DATABASE=maindb;"
    "USER=root;"
    "PASSWORD= mysql;"
)

# --- FUNÇÕES AUXILIARES ---

def conectar_banco():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except pyodbc.Error as ex:
        # Pega o código do erro (SQLSTATE)
        sqlstate = ex.args[0]
        if sqlstate == 'IM002':
            print("ERRO: Driver ODBC do MySQL não encontrado.")
            print("Verifique se o nome do DRIVER na CONNECTION_STRING está correto e se o driver está instalado.")
        else:
            print(f"Erro de conexão com o banco de dados: {ex}")
        sys.exit(1) # Encerra o programa se não puder conectar

def listar_registros(conn, tabela):
    cursor = conn.cursor()
    if tabela == 'USUARIO':
        print("\n--- Usuários Cadastrados ---")
        cursor.execute("SELECT id_usuario, nome, email FROM USUARIO")
        for row in cursor.fetchall():
            print(f"ID: {row.id_usuario} | Nome: {row.nome} | Email: {row.email}")
    elif tabela == 'TAREFA':
        print("\n--- Tarefas Cadastradas ---")
        cursor.execute("SELECT id_tarefa, titulo, status FROM TAREFA")
        for row in cursor.fetchall():
            print(f"ID: {row.id_tarefa} | Título: {row.titulo} | Status: {row.status}")
    cursor.close()

# --- FUNÇÕES DO MENU PRINCIPAL ---

def tela_splash():
    
    print("==========================================")
    print("    SISTEMA DE GERENCIAMENTO DE TAREFAS   ")
    print("==========================================")
    print("\nDesenvolvido por:")
    print("- Cauan Henrique")
    print("- Eduardo Malaquias")
    print("- Guilherme Paiva")
    print("- Júlia Paiva")
    print("- Juliano Dantas")
    print("- Rubiale Filho")
    print("\nCarregando...")
    time.sleep(2)

def verificar_registros_iniciais(conn):
    """(Req 5.c) Conta e exibe a quantidade de registros nas tabelas."""
    
    print("--- Verificação Inicial do Banco de Dados ---")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(1) FROM USUARIO")
        print(f"Usuários cadastrados: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(1) FROM TAREFA")
        print(f"Tarefas cadastradas: {cursor.fetchone()[0]}")
    except pyodbc.Error as e:
        print(f"ERRO: As tabelas não foram encontradas. Execute o script 'schema.sql'. Detalhe: {e}")
        conn.close()
        sys.exit(1)
    cursor.close()
    input("\nPressione Enter para ir ao menu principal...")

def relatorios(conn):
    """(Req 6.a) Exibe o menu de relatórios."""
    
    print("--- Menu de Relatórios ---")
    print("1. Total de tarefas por usuário (Agrupamento)")
    print("2. Detalhes de todas as tarefas (Junção)")
    
    opcao = input("Escolha um relatório: ")
    cursor = conn.cursor()
    
    if opcao == '1':
        print("\n--- Total de Tarefas por Usuário ---")
        query = """
            SELECT u.nome, COUNT(t.id_tarefa) as total
            FROM USUARIO u
            LEFT JOIN TAREFA t ON u.id_usuario = t.id_usuario
            GROUP BY u.nome
            ORDER BY total DESC
        """
        cursor.execute(query)
        print(f"{'Usuário':<30} | {'Nº de Tarefas'}")
        print("-" * 45)
        for row in cursor.fetchall():
            print(f"{row.nome:<30} | {row.total}")

    elif opcao == '2':
        print("\n--- Detalhes de Todas as Tarefas ---")
        query = """
            SELECT t.id_tarefa, t.titulo, t.status, u.nome as usuario, c.nome as categoria
            FROM TAREFA t
            JOIN USUARIO u ON t.id_usuario = u.id_usuario
            JOIN CATEGORIA c ON t.categoria_id = c.id
            ORDER BY u.nome, t.id_tarefa
        """
        cursor.execute(query)
        print(f"{'ID':<4} | {'Título':<30} | {'Status':<15} | {'Usuário':<20} | {'Categoria'}")
        print("-" * 90)
        for row in cursor.fetchall():
            print(f"{row.id_tarefa:<4} | {row.titulo:<30} | {row.status:<15} | {row.usuario:<20} | {row.categoria}")

    else:
        print("Opção inválida.")
        
    cursor.close()
    input("\nPressione Enter para voltar ao menu principal...")

def inserir_registros(conn):

    print("--- Inserir Novo Registro ---")
    print("1. Inserir novo USUÁRIO")
    print("2. Inserir nova TAREFA")
    opcao = input("O que deseja inserir? ")
    
    cursor = conn.cursor()
    try:
        if opcao == '1':
            nome = input("Nome do usuário: ")
            email = input("Email: ")
            senha = input("Senha: ")
            cursor.execute("INSERT INTO USUARIO (nome, email, senha) VALUES (?, ?, ?)", nome, email, senha)
            print("Usuário inserido com sucesso!")
        
        elif opcao == '2':
            listar_registros(conn, 'USUARIO')
            usuario_id = int(input("Digite o ID do usuário para esta tarefa: "))
            
            # No modelo simples, a categoria é fixa (1=Trabalho, 2=Estudo, 3=Pessoal)
            print("Categorias disponíveis: 1-Trabalho, 2-Estudo, 3-Pessoal")
            categoria_id = int(input("Digite o ID da categoria: "))
            
            titulo = input("Título da tarefa: ")
            descricao = input("Descrição: ")
            data_inicio = input("Data de início (YYYY-MM-DD) [opcional]: ")
            data_fim = input("Data de fim (YYYY-MM-DD) [opcional]: ")
            cursor.execute(
                "INSERT INTO TAREFA (titulo, descricao, data_inicio, data_fim, status, id_usuario, categoria_id) VALUES (?, ?, ?, ?, 'pendente', ?, ?)",
                titulo, descricao, data_inicio, data_fim, usuario_id, categoria_id
            )
            print("Tarefa inserida com sucesso!")
        
        else:
            print("Opção inválida.")
            return

        conn.commit()
    except (pyodbc.Error, ValueError) as e:
        conn.rollback()
        print(f"ERRO ao inserir: {e}")
    finally:
        cursor.close()
    
    input("\nPressione Enter para voltar ao menu principal...")

def remover_registros(conn):    
    print("--- Remover Registro ---")
    print("1. Remover USUÁRIO")
    print("2. Remover TAREFA")
    opcao = input("O que deseja remover? ")
    
    tabela = ""
    if opcao == '1':
        tabela = "USUARIO"
        listar_registros(conn, tabela)
        try:
            id_remover = int(input(f"Digite o ID do(a) {tabela} que deseja remover: "))

            confirmacao = input(f"Tem CERTEZA que quer remover o registro ID {id_remover}? (s/n): ").lower()
            if confirmacao != 's':
                print("Operação cancelada.")
                return

            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {tabela} WHERE id_usuario = ?", id_remover)
            conn.commit()

            if cursor.rowcount > 0:
                print(f"{tabela} removido com sucesso!")
            else:
                print("Nenhum registro encontrado com este ID.")

        except pyodbc.Error as e:
            if e.args[0] == '23000':
                print("\nERRO: Este usuário não pode ser removido pois possui tarefas associadas a ele.")
                print("Remova ou reatribua as tarefas antes de remover o usuário.")
            else:
                print(f"ERRO ao remover: {e}")
            conn.rollback()
        except ValueError:
            print("ID inválido. Por favor, digite um número.")
   
    elif opcao == '2': 
        tabela = "TAREFA"
        listar_registros(conn, tabela)
        try:
            id_remover = int(input(f"Digite o ID do(a) {tabela} que deseja remover: "))

            confirmacao = input(f"Tem CERTEZA que quer remover o registro ID {id_remover}? (s/n): ").lower()
            if confirmacao != 's':
                print("Operação cancelada.")
                return

            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {tabela} WHERE id_tarefa = ?", id_remover)
            conn.commit()

            if cursor.rowcount > 0:
                print(f"{tabela} removido com sucesso!")
            else:
                print("Nenhum registro encontrado com este ID.")

        except pyodbc.Error as e:
            if e.args[0] == '23000':
                print("\nERRO: Este usuário não pode ser removido pois possui tarefas associadas a ele.")
                print("Remova ou reatribua as tarefas antes de remover o usuário.")
            else:
                print(f"ERRO ao remover: {e}")
            conn.rollback()
        except ValueError:
            print("ID inválido. Por favor, digite um número.")
        else:
            print("Opção inválida.")
            return
    
    input("\nPressione Enter para voltar ao menu principal...")

def atualizar_registros(conn):
    # Para simplificar, vamos focar em atualizar apenas o status da tarefa, que é um caso de uso comum.
    
    print("--- Atualizar Status da Tarefa ---")
    listar_registros(conn, 'TAREFA')
    
    try:
        id_atualizar = int(input("Digite o ID da tarefa que deseja atualizar: "))
        novo_status = input("Digite o novo status (pendente, em_andamento, concluida): ")
        
        if novo_status not in ['pendente', 'em_andamento', 'concluida']:
            print("Status inválido.")
            return

        cursor = conn.cursor()
        cursor.execute("UPDATE TAREFA SET status = ? WHERE id_tarefa = ?", novo_status, id_atualizar)
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Tarefa atualizada com sucesso!")
            # (Req 6.d.7) Mostra o registro atualizado
            cursor.execute("SELECT id_tarefa, titulo, descricao, data_inicio, data_fim, status, tempo_gasto, id_usuario, categoria_id  FROM TAREFA WHERE id_tarefa = ?", id_atualizar)
            row = cursor.fetchone()
            print(f"Atualizado -> ID: {row.id_tarefa} | Título: {row.titulo} | Status: {row.status}")
        else:
            print("Nenhuma tarefa encontrada com este ID.")
            
    except (pyodbc.Error, ValueError) as e:
        print(f"ERRO ao atualizar: {e}")
        conn.rollback()
        
    input("\nPressione Enter para voltar ao menu principal...")

# --- PROGRAMA PRINCIPAL ---

def main():
    tela_splash()
    
    conn = conectar_banco()
    
    verificar_registros_iniciais(conn)
    
    while True:
        print("--- MENU PRINCIPAL ---")
        print("1. Relatórios")
        print("2. Inserir Registros")
        print("3. Remover Registros")
        print("4. Atualizar Status de Tarefa")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            relatorios(conn)
        elif opcao == '2':
            inserir_registros(conn)
        elif opcao == '3':
            remover_registros(conn)
        elif opcao == '4':
            atualizar_registros(conn)
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)

    # Fecha a conexão antes de sair
    conn.close()
    print("Sistema encerrado.")

# Garante que a função main() seja chamada quando o script for executado
if __name__ == "__main__":
    main()
