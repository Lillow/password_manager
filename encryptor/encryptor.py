from cryptography.fernet import Fernet
import os


class Encryptor:
    def __init__(self, key: bytes) -> None:
        self.__cipher = Fernet(key)

    def encrypt(self, plain_text: str) -> bytes:
        """Criptografa o texto plano fornecido."""
        return self.__cipher.encrypt(plain_text.encode())

    def decrypt(self, encrypted_text: bytes) -> str:
        """Descriptografa o texto criptografado fornecido."""
        return self.__cipher.decrypt(encrypted_text).decode()


# Função para gerar uma chave e salvá-la localmente
def __generate_key() -> None:
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Função para carregar a chave já gerada
def load_key() -> bytes:
    if not os.path.exists("secret.key"):
        print("Chave de criptografia não encontrada. Gerando uma nova chave...")
        __generate_key()
    return open("secret.key", "rb").read()
