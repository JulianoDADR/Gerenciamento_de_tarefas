## Rodando no Linux (com `pyodbc` e MySQL)

Este script usa `pyodbc` para se conectar a um banco de dados MySQL. Para executá-lo no Linux, você precisa instalar e configurar corretamente o gerenciador `unixODBC` e o driver ODBC oficial do MySQL.

### 1\. Pré-requisitos

  * Python 3 e `pip` instalados.
  * Um servidor MySQL acessível (local ou remoto).
  * O *schema* do banco de dados (tabelas `USUARIO`, `TAREFA`, etc.) já deve ter sido criado no seu `DATABASE`.

### 2\. Instalação das Dependências

Primeiro, instale as bibliotecas de sistema necessárias: o gerenciador `unixODBC` e o driver ODBC do MySQL.

**Para Debian/Ubuntu:**

-bash
sudo apt update
sudo apt install unixodbc odbc-mysql


*(Nota: O pacote pode ter um nome ligeiramente diferente, como `mysql-connector-odbc` em algumas versões)*

**Para Fedora/RHEL/CentOS:**

-bash
sudo dnf install unixODBC mysql-connector-odbc

### 3\. Instalação do `pyodbc` (Recomendado)

Para baixar a biblioteca é necessário a criação de um ambiente virtual:

# Crie um ambiente virtual
python3 -m venv venv

# Ative o ambiente
source venv/bin/activate

# Instale o pyodbc
pip install pyodbc


### 4\. Configuração do Script

O passo mais importante é atualizar a `CONNECTION_STRING` no script Python.

1.  **Descubra o nome do Driver:**
    No Linux, o nome do driver é definido pelos arquivos de configuração do `unixODBC`. Para listar os drivers instalados, execute:

    bash
    odbcinst -q -d
    

    A saída será algo como:

    
    [MySQL ODBC 8.0 Unicode Driver]
    

    ou

    
    [MySQL ODBC 8.0 Driver]
    

2.  **Atualize o Script:**
    Copie **exatamente** o nome do driver que apareceu entre colchetes (`[]`) no comando anterior e cole no campo `DRIVER` da sua `CONNECTION_STRING`.

    *Exemplo de alteração no script:*

    python
    # Saída do comando foi [MySQL ODBC 8.0 Unicode Driver]

    CONNECTION_STRING = (
        "DRIVER={MySQL ODBC 8.0 Unicode Driver};" # <--- ATUALIZADO
        "SERVER=localhost;"                      # Verifique o host do seu DB
        "DATABASE=maindb;"                       # Verifique o nome do seu DB
        "USER=root;"                             # Verifique seu usuário
        "PASSWORD=mysql;"                        # Verifique sua senha
    )

    **Você pode verificar as credenciais nas instruções do ambiente no arquivo .txt na área de trabalho**
    

    **Atenção:** O nome do driver no seu script (`MySQL ODBC 9.4 Unicode Driver`) é muito específico e provavelmente não será o mesmo instalado pelo `apt` ou `dnf`. **Você deve verificar** com o comando `odbcinst -q -d`.

### 5\. Execução

Após salvar as alterações no script (vamos chamá-lo de `app.py`), basta executá-lo:

bash
# certifique-se que o ambiente virtual está ativo
python3 app.py
```
