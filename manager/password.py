class Password:
    def __init__(self, category: str, description: str, login: str, password: str) -> None:
        self.__id: str = None
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
