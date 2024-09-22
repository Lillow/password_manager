class Password:
    def __init__(
        self,
        category: str,
        description: str,
        login: str,
        password: str,
        id: str = None,
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

    @category.setter
    def category(self, category: str):

        self.__category: str = category

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        self.__description: str = description

    @property
    def login(self) -> str:
        return self.__login

    @login.setter
    def login(self, login: str):
        self.__login: str = login

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str):
        self.__password: str = password


class PasswordFilter(Password):
    def __init__(
        self,
        id: str = None,
        category: str = None,
        description: str = None,
        login: str = None,
        password: str = None,
    ) -> None:
        super().__init__(category, description, login, password, id)

    @Password.id.setter
    def id(self, new_id: str):
        # Modificando diretamente o atributo privado usando name mangling
        self._Password__id: str = new_id
