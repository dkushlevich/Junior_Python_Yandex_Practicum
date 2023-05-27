# Yatube REST API 

![](https://img.shields.io/badge/Django-3.2.16-blue)
![](https://img.shields.io/badge/Django_REST_framework-3.12.4-blue)
![](https://img.shields.io/badge/Djoser-2.1.0-blue)
![](https://img.shields.io/badge/Djangorestframework_simplejwt-4.7.2-blue)

Многофункциональный API для социальной сети Yatube.


## Описание функционала
- Аутентификация по JWT-токену
- Получение, cоздание, обновление и удаление публикаций и комментариев;
- Получение информации о сообществах;
- Получение информации о существующих подписках автора;
- Возможность подписываться на пользователей.







## Версии

---
<details>
  <summary>
    API Yatube 0.1 (CRUD)
  </summary>

  <br>
 
  | Ссылка | Цель | Задачи  | Библиотеки|
  | :-----: | :-------------- | :---------- | :-------:|
|  [API Yatube 0.1 (CRUD)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/04_API_Yatube/04_API_Yatube_v_0.1)|Написать API-сервис для проекта Yatube, поддерживающий CRUD для основных моделей проекта|Познакомиться с DRF: разобраться с основами сериализации данных; разобраться в работе view-функций/классов/сетов; научиться работать с SimpleRouter и DefaultRouter; познакомиться с токенами (Authtoken, JWT-токен), библиотекой Djoiser.|![Django](https://img.shields.io/badge/Django-3.2.16-blue)![Django_REST_framework](https://img.shields.io/badge/DRF-3.12.4-blue)![Djoiser](https://img.shields.io/badge/Djoiser-2.1.0-blue)|

</details>

---

<details>
  <summary>
    API Yatube 0.2 (финальная версия)
  </summary>
  
  <br>
  
  | Ссылка | Цель | Задачи  | Библиотеки|
  | :-----: | :-------------- | :---------- | :-------:|
 |  [API Yatube 0.2 (финальная версия)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/04_API_Yatube/04_API_Yatube_v_0.2)|Доработать API-сервис для проекта Yatube: реализовать пермишены, фильтрацию, сортировку и поиск по запросам клиентов, добавить пагинацию ответов от API, установить ограничение количества запросов к API.|Разобраться с Permissions, Throttling, пагинацией и фильтрацией в DRF; научиться генерировать документацию к API-сервисам.|![Django](https://img.shields.io/badge/Django-3.2.16-blue)![Django_REST_framework](https://img.shields.io/badge/DRF-3.12.4-blue)

</details>

---




## Запуск сервера
### Необходимое ПО

* python **3.9.6**
* pip

### Установка

1. Клонировать репозиторий.
   ```
   $ git clone git@github.com:dkushlevich/Practicum-by-Yandex-Python.git
   ```
2. Cоздать и активировать виртуальное окружение:
    ```
      $ cd 04_API_Yatube/04_API_Yatube_v_0.2
      $ python3 -m venv venv
      $ source venv/bin/activate
    ```

3. Установить зависимости из файла requirements.txt:
    ```
    (venv) $ python3 -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```

4. Выполнить миграции:
    ```
    (venv) $ python3 manage.py migrate
    ```
5. Запустить сервер
    ```
    (venv) $ python3 manage.py runserver
    ```
После выполнения вышеперечисленных инструкций проект доступен по адресу http://127.0.0.1:8000/

## Отправка, получение и обновление данных

### Примеры ответов на запросы для неаутентифицированных пользователей

> Для анонимных пользователей возможны только GET-запросы.

1. GET-запрос на эндпоинт http://127.0.0.1:8000/api/v1/posts/
    ```json
    [
    {
        "id": 1,
        "author": "test_user1",
        "image": "http://127.0.0.1:8000/media/posts/photo_2023-03-17_20.53.10.jpeg",
        "text": "Текст тестового поста",
        "pub_date": "2023-03-18T08:55:29.789186Z",
        "group": 1
    },
    {
        "id": 2,
        "author": "test_user2",
        "image": null,
        "text": "Текст тестового поста 2",
        "pub_date": "2023-03-18T09:05:39.315442Z",
        "group": null
    }
    ]
    ```
2. GET-запрос на эндпоинт http://127.0.0.1:8000/api/v1/groups/
     ```json
     [
    {
        "id": 1,
        "title": "Тестовая группа 1",
        "slug": "test_1",
        "description": "Описание тестовой группы 1"
    },
    {
        "id": 2,
        "title": "Тестовая группа 2",
        "slug": "test_2",
        "description": "Описание тестовой группы 2"
    }
    ]
     ```

### Примеры запросов для аутентифицированных пользователей

> Изменение чужого контента запрещено.

1. POST-запрос на эндпоинт http://127.0.0.1:8000/api/v1/posts/ (создание публикации)
   
    Тело запроса:
    ```json
    {
    "text": "Тестовый пост 3",
    "group": 1
    }
    ```
    Ответ эндпоинта:
    
    ```json
    {
    "id": 3,
    "author": "test_user1",
    "image": null,
    "text": "Тестовый пост 3",
    "pub_date": "2023-03-18T09:16:42.536210Z",
    "group": 1
    }
    ```
2. POST-запрос на эндпоинт http://127.0.0.1:8000/api/v1/follow/ (подписка на пользователя)
    Тело запроса:
    ```json
    {
    "following": "test_user2"
    }
    ```
    Ответ эндпоинта:
    ```json
    {
    "user": "test_user1",
    "following": "test_user2"
    }   
    ```
    Ответ эндпоинта при попытке создать не уникальную подписку:
    ```json
    {
    "non_field_errors": [
        "The fields user, following must make a unique set."
    ]
    }
    ```

> Здесь приведено всего несколько базовых случаев работы API.
> Подробная информация доступна после запуска сервера по адресу http://127.0.0.1:8000/redoc/
    


## Контакты

Данила Кушлевич

[![Telegram Badge](https://img.shields.io/badge/-dkushlevich-blue?style=social&logo=telegram&link=https://t.me/dkushlevich)](https://t.me/dkushlevich)
[![Gmail Badge](https://img.shields.io/badge/-dkushlevich@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:dkushlevich@gmail.com)](mailto:dkushlevich@gmail.com)
