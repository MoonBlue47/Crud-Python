import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self, host='localhost', user='root', password='senai@126', db_name='crud_contatos'):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.conn = None
        self.cursor = None

        self.conectar()
        self.criar_banco()
        self.criar_tabela()

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()
            print("Conexão realizada com sucesso!")
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")

    def criar_banco(self):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            # Seleciona o banco de dados criado para as próximas operações
            self.cursor.execute(f"USE {self.db_name}")
            print(f"Banco de dados '{self.db_name}' verificado/criado e selecionado!")
        except Error as e:
            print(f"Erro ao criar/selecionar o banco de dados: {e}")

    def criar_tabela(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS contatos(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                telefone VARCHAR(255) NOT NULL,
                email VARCHAR(150) NOT NULL
            )
            """
            self.cursor.execute(query)
            self.conn.commit()
            print("Tabela 'contatos' verificada/criada com sucesso!")
        except Error as e:
            print(f"Erro ao criar a tabela: {e}")

    def inserir(self, nome, telefone, email):
        try:
            sql = "INSERT INTO contatos(nome, telefone, email) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (nome, telefone, email))
            self.conn.commit()
            print("Contato inserido com sucesso!")
        except Error as e:
            print(f"Erro ao inserir contato: {e}")

    def atualizar(self, id_contato, nome, telefone, email):
        try:
            sql = "UPDATE contatos SET nome=%s, telefone=%s, email=%s WHERE id=%s"
            self.cursor.execute(sql, (nome, telefone, email, id_contato))
            self.conn.commit()
            print("Contato atualizado com sucesso!")
        except Error as e:
            print(f"Erro ao atualizar contato: {e}")

    def excluir(self, id_contato):
        try:
            sql = "DELETE FROM contatos WHERE id=%s"
            self.cursor.execute(sql, (id_contato,))
            self.conn.commit()
            print("Contato excluído com sucesso!")
        except Error as e:
            print(f"Erro ao excluir contato: {e}")

    def listar(self):
        try:
            self.cursor.execute("SELECT * FROM contatos")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erro ao listar contatos: {e}")
            return []

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()