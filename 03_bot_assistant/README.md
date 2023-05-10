# Homework Bot
![!PTB](https://img.shields.io/badge/python_telegram_bot-13.9.10-blue) 
![!Requests](https://img.shields.io/badge/requests-2.26.0-blue)

## Описание проекта
Homework Bot - телеграм-бот для проверки статуса домашней работы через API-сервис Практикум.Домашка. 

## Что умеет делать бот?
- Раз в 10 минут опрашивает API сервис Практикум.Домашка и проверет статус отправленной на ревью домашней работы;
- При обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- Логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

## Запуск сервера

 Для MacOs и Linux вместо python использовать python3

1. Клонировать репозиторий.
   ```
   git@github.com:dkushlevich/Practicum-by-Yandex-Python.git
   ```
2. Cоздать и активировать виртуальное окружение:
    ```
      $ cd Practicum-by-Yandex-Python/03_bot_assistant
      $ python -m venv venv
    ```
    Для Windows:
    ```
      $ source venv/Scripts/activate
    ```
    Для MacOs/Linux:
    ```
      $ source venv/bin/activate
    ```
3. Установить зависимости из файла requirements.txt:
    ```
    (venv) $ python -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```
4. Импортировать токены для API-сервиса Практикум.Домашка и Telegram
    ```
    export PRACTICUM_TOKEN=<PRACTICUM_TOKEN>
    export TELEGRAM_TOKEN=<TELEGRAM_TOKEN>
    export CHAT_ID=<CHAT_ID>
    ```
    > В случае локального хранения, создайте файл .env и запишите в него ключи

5. Запустить бота
    ```
    python homework.py
    ```

## Контакты
**Данила Кушлевич** 

[![Telegram Badge](https://img.shields.io/badge/-dkushlevich-blue?style=social&logo=telegram&link=https://t.me/dkushlevich)](https://t.me/dkushlevich) [![Gmail Badge](https://img.shields.io/badge/-dkushlevich@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:dkushlevich@gmail.com)](mailto:dkushlevich@gmail.com)
