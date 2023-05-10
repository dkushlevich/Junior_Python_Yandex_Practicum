# Социальная сеть Yatube для публикации личных дневников (v 0.2)
![Python](https://img.shields.io/badge/Python-3.9.10-blue) ![!Django](https://img.shields.io/badge/Django-2.2.9-blue)

## Описание проекта
Социальная сеть для авторов и подписчиков. Пользователи могут подписываться на избранных авторов, оставлять и удалять комментари к постам, оставлять новые посты на главной странице и в тематических группах, прикреплять изображения к публикуемым постам.

## Предыдущие версии

[![V1](https://img.shields.io/badge/Version-0.1-blue?style=flat&link=https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/02_Yatube_v_0.1)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/02_Yatube_v_0.1)

## Нововведения текущей версии
- Добавлено приложение **Users** со следующим функционалом:
    - Регистрации пользователей;
    - Восстановления пароля по email;
    - Изменения пароля;
    - Входа/выхода пользователя.
- Добавлена возможность создавать и редактировать посты;
- Обновлена пагинация;
- Добавлены разделы **"Об авторе"** и **"Технологии".**



## Запуск сервера

 Для MacOs и Linux вместо python использовать python3

1. Клонировать репозиторий.
   ```
   git@github.com:dkushlevich/Practicum-by-Yandex-Python.git
   ```
2. Cоздать и активировать виртуальное окружение:
    ```
      $ cd Practicum-by-Yandex-Python/02_Yatube_v_0.1
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
4. Создать и запустить миграции:
    ```
    cd yatube/
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Запустить сервер:
    ```
    python manage.py runserver
    ```
> После выполнения вышеперечисленных инструкций проект доступен по адресу http://127.0.0.1:8000/

## Контакты

**Данила Кушлевич** 

[![Telegram Badge](https://img.shields.io/badge/-dkushlevich-blue?style=social&logo=telegram&link=https://t.me/dkushlevich)](https://t.me/dkushlevich) [![Gmail Badge](https://img.shields.io/badge/-dkushlevich@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:dkushlevich@gmail.com)](mailto:dkushlevich@gmail.com)
