from rest_framework.exceptions import ValidationError


def validate_username_not_me(value):
    if value.lower() == 'me':
        raise ValidationError(" me - запрещённое имя пользователя")
