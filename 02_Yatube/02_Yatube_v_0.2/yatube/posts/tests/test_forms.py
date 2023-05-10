from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class TaskCreateFormTests(TestCase):
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
            text='Текст тестового поста',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка: Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        data_create = {
            'text': "Созданный в тестовом клиенте пост",
            'group': self.post.group.id
        }
        response = self.authorized_client.post(
            (reverse('posts:post_create')), data_create, follow=True
        )
        created_post = Post.objects.first()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Созданный в тестовом клиенте пост',
                group=self.post.group.id
            ).exists()
        )
        self.assertEqual(created_post.text, data_create['text'])
        self.assertEqual(created_post.group.id, data_create['group'])

    def test_edit_post(self):
        """Проверка: Валидная форма редактирует запись в Post."""
        post_count = Post.objects.count()
        new_group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group'
        )
        data_edit = {
            'text': "Измененный в тестовом клиенте пост",
            'group': new_group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data_edit,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        edited_post = Post.objects.first()
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(edited_post.text, data_edit['text'])
        self.assertEqual(edited_post.group.id, data_edit['group'])

    def test_edit_post(self):
        """Проверка: Форма от неатворизованного пользователя
        не сохраняется в БД
        """
        post_count = Post.objects.count()
        data_create = {
            'text': "Созданный в тестовом клиенте пост",
            'group': self.post.group.id
        }
        response = self.guest_client.post(
            (reverse('posts:post_create')), data_create
        )
        reverse_login = reverse('users:login')
        self.assertRedirects(response, f'{reverse_login}?next=/create/')
        self.assertEqual(post_count, Post.objects.count())
