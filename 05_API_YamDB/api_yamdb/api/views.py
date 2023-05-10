from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdministrator
from api.serializers import SignUpSerializer, TokenSerializer, UserSerializer
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdministrator,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username', )

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if 'role' in serializer.validated_data:
            serializer.validated_data.pop('role')
        serializer.save()
        return Response(serializer.data)


class SignUpView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            try:
                user, _ = User.objects.get_or_create(
                    email=email,
                    username=username
                )
            except IntegrityError:
                raise serializers.ValidationError(
                    {'message': 'Пользователь с такими данными уже существует'}
                )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Confirmation Code',
                message=f'Ваш код активации: {confirmation_code}',
                recipient_list=[email, ],
                from_email='YamDB@example.com',
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                return Response(
                    {'Bearer': f'{token}'}
                )
            return Response(
                {'message': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
