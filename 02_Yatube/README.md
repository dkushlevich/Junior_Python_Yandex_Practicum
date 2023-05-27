# Социальная сеть Yatube для публикации личных дневников <br> [Деплой проекта](http://dkushlevich.pythonanywhere.com)
![Python](https://img.shields.io/badge/Python-3.9.10-blue) ![!Django](https://img.shields.io/badge/Django-2.2.9-blue)


## Описание проекта
Социальная сеть для авторов и подписчиков. Пользователи могут подписываться на избранных авторов, оставлять и удалять комментари к постам, оставлять новые посты на главной странице и в тематических группах, прикреплять изображения к публикуемым постам.

## Версии


<details>
  <summary>
    Yatube v 0.1 (сообщества)
  </summary>

  <br>
 
  | Ссылка | Цель | Задачи  | Библиотеки|
  | :-----: | :-------------- | :---------- | :-------:|
 |  [Yatube v 0.1 (сообщества)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/02_Yatube/02_Yatube_v_0.1)|Создать общую архитектуру социальной сети Yatube для ведения личных дневников.| Сделать первые шаги в Django; разобраться с моделью MTV; научиться работать с миграциями; прикоснуться к Django ORM; посмотреть на принципы верстки для бэкенда (HTML, CSS, Bootstrap).| ![!Django](https://img.shields.io/badge/Django-2.2.9-blue)  |

</details>

---

<details>
  <summary>
    Yatube v 0.2 (новые записи) 
  </summary>
  
  <br>
  
  | Ссылка | Цель | Задачи  | Библиотеки|
  | :-----: | :-------------- | :---------- | :-------:|
  |  [Yatube v 0.2 (новые записи)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/02_Yatube/02_Yatube_v_0.2)|Разработать дополнительный функционал для Yatube: создать ресурс для работы с пользователями, настроить пагинацию, добавить возможность пользователям создавать и редактировать собственные посты.|Подробнее разобраться в Django ORM (CRUD, фильтрация, агрегирующие функции, оптимизация запросов); научиться работать с Shell в рамках Django; научиться использовать Generic Views; разобраться с встроенным паджинатором; научиться создавать контекст-процессоры; подробно разобраться с возможностями приложения django.contrib.auth, научиться работать с формами | ![!Django](https://img.shields.io/badge/Django-2.2.9-blue) |

</details>

---

<details>
  <summary>
    Yatube v 0.3 (покрытие тестами)
  </summary>
  
  <br>
  
  | Ссылка | Цель | Задачи  | Библиотеки|
  | :-----: | :-------------- | :---------- | :-------:|
  |  [Yatube v 0.3 (покрытие тестами)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/02_Yatube/02_Yatube_v_0.3)        |Протестировать созданный ранее функционал Yatubе|Познакомиться с принципом TDD и библиотекой Unittest; научиться писать атомарные, независимые, вариатиивные и неизбыточные тесты. |![!Django](https://img.shields.io/badge/Django-2.2.9-blue) |

</details>

---

<details>
  <summary>
    Yatube v 0.4 (подписки на авторов)
  </summary>
  
  <br>
 
  | Ссылка | Цель | Задачи  | Библиотеки|
  | :-----: | :-------------- | :---------- | :-------:|
  |  [Yatube v 0.4 (подписки на авторов)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/02_Yatube/02_Yatube_v_0.4)|Расширить возможности Yatube: разработать функционал, позволяющий пользователям добавлять каритнки к постам, комментировать посты и подписываться друг на друга; добавить кеширование; написать тесты к нововведениям. Провести рефакторинг проекта. | Познакомиться с библиотекой для работы с графикойsorl-thumbnail. Научиться проводить рефакторинг собственного кода: разобраться с принципами DRY, KISS, YAGNI; Научиться кешировать данные; Научиться пользоваться django-debug-toolbar|![!Django](https://img.shields.io/badge/Django-2.2.9-blue) |

</details>

---

<details>
  <summary>
    Yatube v 1.0 (финальная версия)
  </summary>
  
  <br>
 
  | Ссылка | Цель | Задачи  | Библиотеки|
  | :-----: | :-------------- | :---------- | :-------:|
  |  [Yatube v 1.0 (финальная версия)](https://github.com/dkushlevich/Practicum-by-Yandex-Python/tree/main/02_Yatube/02_Yatube_v_1.0_custom)|Доработать проект Yatube с учётом личных пожеланий, значительно расширить возможности проекта. Переписать все view-функции на CBV, полностью изменить оформление сайта, добавить личный кабинет пользователя с возможностью установки аватара, добавить лайки к комментариям и постам.|Разработать и выполнить собственное ТЗ. Реализовать идеи, которые хотелось попробовать в ходе основного проекта.|![!Django](https://img.shields.io/badge/Django-2.2.9-blue) |

</details>

---



## Запуск сервера

 Для MacOs и Linux вместо python использовать python3

1. Клонировать репозиторий.
   ```
   git@github.com:dkushlevich/Practicum-by-Yandex-Python.git
   ```
2. Cоздать и активировать виртуальное окружение:
    ```
      $ cd Practicum-by-Yandex-Python/02_Yatube_v_1.0
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

