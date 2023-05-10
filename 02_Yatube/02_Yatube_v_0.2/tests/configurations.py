
dict_for_runserver={
    "name": "Yatube",
            "type": "python",
            "request": "launch",
            "program": "Полный путь до manage.py проекта",
            "python": "Полный путь до python3 в venv проекта - например (Путь до папки)/hw03_forms/venv/bin/python3",
            "console": "internalConsole",
            "args": [
                "runserver"
            ]
}

dict_for_test={
            "name": "Python: Django Debug Single Test",
            "type": "python",
            "request": "launch",
            "program": "Полный путь до manage.py проекта",
            "args": [
                "test",
                "ОТНОСИТЕЛЬНЫЙ путь до папки tests, тесты которой вы хотите проверить"
            ],
            "django": true
        }