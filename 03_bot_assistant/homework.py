import json
import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (ApiResponseFormatError, ApiResponseKeyError,
                        ServerApiError, VerdictKeyError)

load_dotenv()

logger = logging.getLogger(__name__)

PRACTICUM_TOKEN: str = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID: int = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD: int = 600
ENDPOINT: str = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS: dict = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS: dict = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

TYPE_ERROR_MESSAGE: str = ('Ошибка типа данных в ответе сервера. '
                           'Ожидаемый тип данных:{}, полученный тип {}')


def check_tokens() -> bool:
    """Проверяет доступность переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, ENDPOINT, TELEGRAM_CHAT_ID])


def send_message(bot: telegram.Bot, message: str) -> None:
    """Отправляет сообщение в Telegramm чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'Отправлено сообщение "{message}"')
    except telegram.error.TelegramError as error:
        logger.error(error)


def get_api_answer(timestamp: int) -> dict:
    """Делает запрос к эндпоинту API-сервиса ЯП."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(url=ENDPOINT, headers=HEADERS, params=payload)
    except requests.RequestException:
        raise ServerApiError(response.status_code)
    if not response.status_code == HTTPStatus.OK:
        raise ServerApiError(response.status_code)
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        raise ApiResponseFormatError


def check_response(response: dict) -> None:
    """Проверяет API на соотетствие документации."""
    if not isinstance(response, dict):
        message_error = TYPE_ERROR_MESSAGE.format(type(response), dict)
        raise TypeError(message_error)
    if 'homeworks' not in response:
        raise ApiResponseKeyError('homeworks')
    if not isinstance(response['homeworks'], list):
        message_error = TYPE_ERROR_MESSAGE.format(
            type(response['homeworks']),
            list
        )
        raise TypeError(message_error)


def parse_status(homework: dict) -> str:
    """Извлекает из информации о домашней работе статус этой работы."""
    if 'homework_name' not in homework:
        raise ApiResponseKeyError('homework_name')
    homework_name = homework['homework_name']
    if 'status' not in homework:
        raise ApiResponseKeyError('status')
    hw_status = homework['status']
    if hw_status not in HOMEWORK_VERDICTS:
        raise VerdictKeyError(hw_status)
    verdict = HOMEWORK_VERDICTS[hw_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Переменная окружения не обнаружена')
        sys.exit()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    message_list = []
    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            homework = response['homeworks'][0]
            message = parse_status(homework)
            send_message(bot, message)
            timestamp = response['current_date']
        except IndexError:
            logger.debug('Статус работы не изменился')
        except Exception as error:
            logger.error(error)
            message = f'Сбой в работе программы: {error}'
            if message not in message_list:
                send_message(bot, message)
                message_list.append(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s, %(levelname)s, %(message)s, %(funcName)s, '
            '%(lineno)s, %(name)s'
        ),
        stream=sys.stdout
    )
    main()
