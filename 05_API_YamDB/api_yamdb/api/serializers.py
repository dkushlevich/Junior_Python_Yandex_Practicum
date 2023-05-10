from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import User
from reviews.validators import validate_username_not_me


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[User.username_validator, validate_username_not_me],
        max_length=150)

    email = serializers.EmailField(
        max_length=254
    )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()),
                    User.username_validator,
                    validate_username_not_me],
        max_length=150
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
