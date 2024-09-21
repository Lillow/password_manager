from cryptography.fernet import Fernet
import os


class Encryptor:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, plain_text: str) -> bytes:
        """Criptografa o texto plano fornecido."""
        return self.cipher.encrypt(plain_text.encode())

    def decrypt(self, encrypted_text: bytes) -> str:
        """Descriptografa o texto criptografado fornecido."""
        return self.cipher.decrypt(encrypted_text).decode()


# Função para gerar uma chave e salvá-la localmente
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Função para carregar a chave já gerada
def load_key():
    if not os.path.exists("secret.key"):
        print("Chave de criptografia não encontrada. Gerando uma nova chave...")
        generate_key()
    return open("secret.key", "rb").read()


if __name__ == "__main__":
    # Apenas para teste: gerar uma chave se ainda não existir
    generate_key()
    print("Chave gerada e salva em 'secret.key'.")
