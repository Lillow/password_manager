class Password:
    def __init__(
        self,
        category: str,
        description: str,
        login: str,
        password: str,
        id=None,
    ) -> None:
        self.__id: str = id
        self.__category: str = category
        self.__description: str = description
        self.__login: str = login
        self.__password: str = password

    @property
    def id(self) -> str:
        return self.__id

    @property
    def category(self) -> str:
        return self.__category

    @property
    def description(self) -> str:
        return self.__description

    @property
    def login(self) -> str:
        return self.__login

    @property
    def password(self) -> str:
        return self.__password


class PasswordFilter(Password):
    def __init__(
        self,
        id: str = None,
        category: str = None,
        description: str = None,
        login: str = None,
        password: str = None,
    ) -> None:
        super().__init__(category, description, login, password)

    @Password.id.setter
    def id(self, new_id: str):
        # Modificando diretamente o atributo privado usando name mangling
        self._Password__id: str = new_id

    @Password.category.setter
    def category(self, new_category: str):
        self._Password__category: str = new_category

    @Password.description.setter
    def description(self, new_description: str):
        self._Password__description: str = new_description

    @Password.login.setter
    def login(self, new_login: str):
        self._Password__login: str = new_login
