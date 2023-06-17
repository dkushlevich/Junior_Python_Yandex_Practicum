<div align=center>
  
# [Kittygram](https://kittygramhostname.ddns.net/signin)

![Python](https://img.shields.io/badge/Python-3.9.10-blue)
![Django](https://img.shields.io/badge/Django-3.2.16-blue)
![Django_REST_framework](https://img.shields.io/badge/Django_REST_framework-3.12.4-blue)
![Nginx](https://img.shields.io/badge/Nginx-1.18.0-blue)
![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1.0-blue)
</div>


## Описание проекта

Kittygram - SPA, предназначенное для всех, кто увлекается котиками и хочет делиться фотографиями и достижениями своих питомцев с другими пользователями. 

В Kittygram предоставлены интерфейсы для регистрации новых и для аутентификации зарегистрированных пользователей.

Аутентифицированным пользователям проект позволяет добавлять новых питомцев на сайт.

Для каждого нового котика нужно указать его имя, год рождения и достижения(выбрать из уже существующих или создать новое), выбрать цвет . Опционально можно загрузить фотографию своего питомца; для котиков без фотографии будет выводиться изображение по умолчанию.
Информацию о собственных котах можно изменить или вовсе удалить с сайта.

На одной странице отображается не более десяти котиков.

Все вышеперечисленные возможности работают на базе API ([документация](https://kittygramhostname.ddns.net/redoc/))

## Ресурсы API

* Ресурс **cats**: котики
* Ресурс **achivements**: достижения котиков
* Ресурс **users**: пользователи
* Ресурс **token**: создание токена


<details>
  <summary>
    <h2>Запуск проекта на локальном сервере</h2>
  </summary>

<details>
  <summary>
    <h3>Запуск бэкенда</h3>
  </summary>


> Для MacOs и Linux вместо python использовать python3

1. Клонировать репозиторий.
   ```
   $ git clone git@github.com:dkushlevich/infra_sprint1.git
   ```
2. Cоздать и активировать виртуальное окружение:
    ```
      $ cd backend/
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
3. Установить зависимости:
    ```
    (venv) $ python -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```
4. Создать секретный ключ приложения:
    * Создать файл .env в папке ```/infra_sprint1/backend```
    * Сгенерировать секретный ключ с помощью команды:
        ```
        (venv) $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
        ```
    *  Записать полученный ключ в файл .env по принципу:
        ```
        SECRET_KEY=<Ваш секретный ключ>
        ```
        > Без пробелов и <>

5. Разрешить CORS:

    * Установить пакет django-cors-headers в виртуальном окружении:
        ```
        (venv) $ pip install django-cors-headers 
        ```
        
    *  Подключить его в settings.py:
        ```py
        INSTALLED_APPS = [
            ...
            'rest_framework',
            'corsheaders',
            ...
            ] 
        ```
    * В списке MIDDLEWARE (файл settings.py) зарегистрировать обработчик CorsMiddleware. Он должен быть размещён выше CommonMiddleware:
        ```py
        MIDDLEWARE = [
            ...
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            ...
        ]
        ```
    * Разрешить обрабатывать запросы, приходящие c localhost:3000 для api/ (файл settings.py):
        
        ```py
            CORS_URLS_REGEX = r'^/api/.*$'
            CORS_ALLOWED_ORIGINS = [
                'http://localhost:3000',
            ] 
        ```

5. Выполнить миграции:
    ```
    (venv) $ python manage.py migrate
    ```

6. Загрузить статику
    ```
    (venv) $ python manage.py collectstatic
    (venv) $ python manage.py generateschema > static_backend/redoc.yaml
    ```
7. Запустить сервер:
    ```
    (venv) $ python manage.py runserver
    ```
После выполнения вышеперечисленных инструкций бэкенд проекта будет доступен по адресу http://127.0.0.1:8000/

> Подробная документация API доступна после запуска сервера по адресу http://127.0.0.1:8000/redoc/

</details>

---

<details>
  <summary>
    <h3>Подключение фронтенда</h3>
  </summary>

1. Разрешить CORS:

    * Установить пакет django-cors-headers в виртуальном окружении:
        ```
        (venv) $ pip install django-cors-headers 
        ```
        
    *  Подключить его в settings.py:
        ```py
        INSTALLED_APPS = [
            ...
            'rest_framework',
            'corsheaders',
            ...
            ] 
        ```
    * В списке MIDDLEWARE (файл settings.py) зарегистрировать обработчик CorsMiddleware. Он должен быть размещён выше CommonMiddleware:
        ```py
        MIDDLEWARE = [
            ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
        ]
        ```
    * Разрешить обрабатывать запросы, приходящие c localhost:3000 для api/ (файл settings.py):
        
        ```py
            CORS_URLS_REGEX = r'^/api/.*$'
            CORS_ALLOWED_ORIGINS = [
                'http://localhost:3000',
            ] 
        ```
2. Перейти в папку /infra_sprint1/frontend и установить зависимости:
    
    ```
        npm -i
    ```
3. Запустить проект: 
    
    ```
        npm run start
    ```
    После выполнения вышеперечисленных инструкций проект будет доступен по адресу http://localhost:3000
    </details>
 </details>

---

<details>
  <summary>
    <h2>Запуск проекта на удалённом сервере</h2>
  </summary>


1. Подключиться к удалённому серверу (Linux Ubuntu 22.04 с публичным ip):
   ```
   $ ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом_без_расширения login@ip
   ```

2. Клонировать репозиторий:
   ```
   $ git clone git@github.com:dkushlevich/infra_sprint1.git
   ```
3. Cоздать и активировать виртуальное окружение:
    ```
      $ cd backend/
      $ python -m venv venv
      $ source venv/bin/activate
    ```
4. Установить зависимости:
    ```
    (venv) $ python -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```
5. Создать секретный ключ приложения:
    * Создать файл .env в папке ```/infra_sprint1/backend```
    * Сгенерировать секретный ключ с помощью команды:
        ```
        (venv) $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
        ```
    *  Записать полученный ключ в файл .env по принципу:
        ```
        SECRET_KEY=<Ваш секретный ключ>
        ```
        > Без пробелов и <>

6. Выполнить миграции:
    ```
    (venv) $ python manage.py migrate
    ```

7. Установить Gunicorn:
    ```
    pip install gunicorn==20.1.0
    ```
8. Создать юнит для Gunicorn:
    ```
    sudo nano /etc/systemd/system/gunicorn_kittygram.service 
    ```
    Прописать
    ```
    [Unit]
    Description=gunicorn daemon 
    After=network.target 

    [Service]
    User=<Имя пользователя> 
    
    WorkingDirectory=<Путь к директории проекта>
    
    ExecStart=<директория-с-проектом>/<путь-до-gunicorn-в-виртуальном-окружении> --bind 0.0.0.0:8000 kyttygram_backend.wsgi
    
    [Install]
    WantedBy=multi-user.target
    ```

9. Запустить созданный юнит:
    ```
    sudo systemctl start gunicorn_kittygram     
    ```

10. Установить Nginx:
    ```
    sudo apt install nginx -y 
    ```
11. Настроить и запустить файрвол:
    ```
    sudo ufw allow 'Nginx Full'
    sudo ufw allow OpenSSH
    sudo ufw enable
    ```
12. Собрать статику фронтенд-приложения и скопировать её в системную директорию Nginx:

    * Перейти в директорию taski/frontend и выполнить команду:
        ```
            npm run build
        ```
        
    * Скопировать созданную папку в /var/www
        ```
        sudo cp -r /infra_sprint1/frontend/build/. /var/www/kittygram/ 
        ```
        
13. Прописать конфиг веб-сервера:
    ```
     sudo nano /etc/nginx/sites-enabled/default
    ```
    
    ```
    server {
        server_name kittygramhostname.ddns.net;
        server_tokens off;
        client_max_body_size 20M;

        location /media {
            autoindex on;
            alias /var/www/kittygram/media/;
        }

        location /admin/ {
            proxy_pass http://127.0.0.1:8000;
        }
    
        location /api/ {
            proxy_pass http://127.0.0.1:8000;
        }
    
        location /redoc/ {
            proxy_pass http://127.0.0.1:8000;
        }
    
        location / {
            root   /var/www/kittygram;
            index  index.html index.htm;
            try_files $uri /index.html;
        }
    }
    ```
14. Перезагрузить Nginx:
    ```
    sudo systemctl reload nginx
    ```
    
15. Собрать статику и перенести её в Nginx:
    ```
    (venv) $ python manage.py collectstatic
    (venv) $ python manage.py generateschema > static_backend/redoc.yaml
    ```
    ```
        sudo cp -r /infra_sprint1/backend/static_backend/. /var/www/kittygram/
    ```

16. Cоздать директорию media в директории /var/www/kittygram/
  
17. При необходимости настроить SSL-соединение.


> Подробная документация API доступна после запуска сервера по адресу http://<ваш IP/домен>/redoc/
  </details>

---

<div align=center>

## Контакты

[![Telegram Badge](https://img.shields.io/badge/-dkushlevich-blue?style=social&logo=telegram&link=https://t.me/dkushlevich)](https://t.me/dkushlevich) [![Gmail Badge](https://img.shields.io/badge/-dkushlevich@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:dkushlevich@gmail.com)](mailto:dkushlevich@gmail.com)

</div>

