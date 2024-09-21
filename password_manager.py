import sqlite3
from encryptor import Encryptor, load_key


class PasswordManager:
    def __init__(self, db_path="database/password_db.sqlite"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

        # Carregar a chave e inicializar o criptografador
        self.key = load_key()
        self.encryptor = Encryptor(self.key)

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        login TEXT NULL,
                        encrypted_password TEXT NOT NULL
                    );"""
        self.conn.execute(query)
        self.conn.commit()

    def add_password(self, category, description, login, plain_password):
        """Adiciona uma nova senha criptografada ao banco de dados."""
        encrypted_password = self.encryptor.encrypt(plain_password)
        query = "INSERT INTO passwords (category, description, login, encrypted_password) VALUES (?, ?, ?, ?);"
        self.conn.execute(query, (category, description, login, encrypted_password))
        self.conn.commit()

    def get_password(self, id):
        """Recupera e descriptografa a senha pelo ID."""
        query = "SELECT category, description, login, encrypted_password FROM passwords WHERE id = ?;"
        cursor = self.conn.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            category, description, login, encrypted_password = result
            decrypted_password = self.encryptor.decrypt(encrypted_password)
            return {
                "category": category,
                "description": description,
                "login": login,
                "password": decrypted_password,
            }
        return None

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Inicializando o gerenciador de senhas e adicionando um exemplo
    manager = PasswordManager()
    print("Banco de dados configurado com sucesso!")

    # Exemplo de como adicionar uma senha criptografada
    manager.add_password(
        "Social", "Minha conta do Facebook", "meu_login", "minha_senha123"
    )
    print("Senha adicionada com sucesso!")

    # Exemplo de como consultar e descriptografar a senha
    senha = manager.get_password(1)
    if senha:
        print("Dados recuperados:", senha)

    manager.close()
