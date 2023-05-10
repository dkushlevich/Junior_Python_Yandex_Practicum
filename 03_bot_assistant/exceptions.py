class ApiResponseKeyError(Exception):
    MESSAGE = 'Отсутствие ключа в ответе сервиса ЯП'

    def __init__(self, key) -> None:
        self.key = key

    def __str__(self) -> str:
        return f'{self.MESSAGE}: {self.key}'


class VerdictKeyError(KeyError):
    MESSAGE = 'Полученный статус работы не соответсвует ожидаемым'

    def __init__(self, key) -> None:
        self.key = key

    def __str__(self) -> str:
        return f'{self.MESSAGE}: {self.key}'


class ServerApiError(Exception):
    MESSAGE = 'Неполадки на сервере'

    def __init__(self, status_code: str) -> None:
        self.status_code = status_code

    def __str__(self) -> str:
        return f'{self.MESSAGE}. Код запроса: {self.status_code}'


class ApiResponseFormatError(Exception):
    MESSAGE = 'Формат ответа не JSON'

    def __str__(self) -> str:
        return f'{self.MESSAGE}'
