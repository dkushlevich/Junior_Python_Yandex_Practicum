from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    fixtures = [
        'posts.xml',
        'groups.xml',
        'users.xml'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.last()
        cls.user = User.objects.create(username='test_user')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.url_template = {
            '/': 'posts/index.html',
            f'/group/{cls.post.group.slug}/': 'posts/group_list.html',
            f'/posts/{cls.post.id}/': 'posts/post_detail.html',
            f'/profile/{cls.post.author}/': 'posts/profile.html',
            f'/posts/{cls.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html'
        }
        cls.urls_for_all = (
            '/',
            f'/group/{cls.post.group.slug}/',
            f'/posts/{cls.post.id}/',
            f'/profile/{cls.post.author}/'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_not_author = Client()
        not_author_user = User.objects.create(username='not_author')
        self.authorized_client_not_author.force_login(not_author_user)

    def test_unexisting_page(self):
        """Проверка: запрос к несуществующей странице
        возвращает ошибку 404
        """
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_exists_at_desired_location_anonymous(self):
        """Проверка: страницы доступны всем"""
        for url in self.urls_for_all:
            response = self.guest_client.get(url)
            with self.subTest(url=url):
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_post_exists_at_desired_location_authorized(self):
        """Проверка: страница создания поста доступна
        авторизованному пользователю
        """
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_post_exists_at_desired_location_author(self):
        """Проверка: страница изменения поста доступна
        автору поста
        """
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_post_redirect_anonymous_on_login(self):
        """Проверка: cтраница по адресу /create/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_edit_post_redirect_on_post_profile_none_author(self):
        """Проверка: страница по адресу /edit/ перенаправит пользователя,
        не являющегося автором данного поста, на страницу просмотра поста
        """
        response = self.authorized_client_not_author.get(
            f'/posts/{self.post.id}/edit/', follow=True
        )
        self.assertRedirects(
            response, f'/posts/{self.post.id}/'
        )

    def test_urls_uses_correct_template(self):
        """Проверка: URL-адрес использует соответствующий шаблон."""
        for url, template in self.url_template.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
