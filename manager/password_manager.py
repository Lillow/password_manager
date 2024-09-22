import sqlite3
from unittest.mock import patch
from encryptor.encryptor import Encryptor, load_key
from os import path, getcwd, makedirs


class PasswordManager:
    def __init__(self, db_path="database/password_db.sqlite") -> None:
        self._conn: sqlite3.Connection = self._db_connect(db_path)
        self._create_table()

        # Carregar a chave e inicializar o criptografador
        self._key: bytes = load_key()
        self._encryptor = Encryptor(self._key)

    def _db_connect(self, db_path) -> sqlite3.Connection:
        patch = path.join(getcwd(), "database")
        if not path.exists(patch):
            makedirs(patch)
        return sqlite3.connect(db_path)

    def _create_table(self) -> None:
        query = """CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY key AUTOINCREMENT,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        login TEXT NULL,
                        encrypted_password TEXT NOT NULL
                    );"""
        self._conn.execute(query)
        self._conn.commit()

    def add_password(self, category, description, login, plain_password) -> None:
        """Adiciona uma nova senha criptografada ao banco de dados."""
        encrypted_password = self._encryptor.encrypt(plain_password)
        query = "INSERT INTO passwords (category, description, login, encrypted_password) VALUES (?, ?, ?, ?);"
        self._conn.execute(query, (category, description, login, encrypted_password))
        self._conn.commit()

    def get_password(self, id):
        """Recupera e descriptografa a senha pelo ID."""
        query = "SELECT category, description, login, encrypted_password FROM passwords WHERE id = ?;"
        cursor = self._conn.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            category, description, login, encrypted_password = result
            decrypted_password = self._encryptor.decrypt(encrypted_password)
            return {
                "category": category,
                "description": description,
                "login": login,
                "password": decrypted_password,
            }
        return None

    def upd_password(
        self,
        id,
        new_category=None,
        new_description=None,
        new_login=None,
        new_plain_password=None,
    ):

        query = "SELECT encrypted_password FROM passwords WHERE id = ?;"
        cursor = self._conn.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            # Atualizar os valores que foram fornecidos (os que não forem, mantêm os atuais)
            query_update = """UPDATE passwords SET 
                                    category = COALESCE(?, category),
                                    description = COALESCE(?, description),
                                    login = COALESCE(?, login),
                                    encrypted_password = COALESCE(?, encrypted_password)
                                WHERE id = ?;"""

            # Se uma nova senha for passada, criptografá-la
            if new_plain_password:
                new_encrypted_password = self._encryptor.encrypt(new_plain_password)
            else:
                new_encrypted_password = None

            # Executar a atualização
            self._conn.execute(
                query_update,
                (new_category, new_description, new_login, new_encrypted_password, id),
            )
            self._conn.commit()
            return True
        return False

    def del_password(self, id) -> bool:
        """Deleta uma senha pelo ID."""
        query = "DELETE FROM passwords WHERE id = ?;"
        cursor = self._conn.execute(query, (id,))
        self._conn.commit()

        # Verificar se alguma linha foi afetada
        return cursor.rowcount > 0

    def _close(self) -> None:
        self._conn.close()


def main():
    # Inicializando o gerenciador de senhas e adicionando um exemplo
    manager = PasswordManager()
    # print("Banco de dados configurado com sucesso!")

    # Exemplo de como adicionar uma senha criptografada
    # manager.add_password(
    #     "Social", "Minha conta do Facebook", "meu_login", "minha_senha123"
    # )
    # print("Senha adicionada com sucesso!")

    # Exemplo de como consultar e descriptografar a senha
    # senha = manager.get_password(1)
    # if senha:
    #     print("Dados recuperados:", senha)

    # Exemplo de como alterar senha
    # manager.upd_password(1, new_category="Novo Categoria", new_description="Nova descrição", new_plain_password="nova_senha123")

    # Exemplo de como deletar
    manager.del_password(1)

    manager._close()
