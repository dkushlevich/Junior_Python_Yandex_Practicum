import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Group, Post

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    fixtures = [
        'posts.xml',
        'groups.xml',
        'users.xml',
        'comments.xml'
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка: Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif')
        data_create = {
            'text': "Созданный в тестовом клиенте пост",
            'group': self.post.group.id,
            'image': uploaded
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
                group=self.post.group.id,
                image='posts/small.gif'
            ).exists()
        )
        self.assertEqual(created_post.text, data_create['text'])
        self.assertEqual(created_post.group.id, data_create['group'])
        self.assertEqual(created_post.image, 'posts/small.gif')

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

    def test_edit_post_anonymous(self):
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
        self.assertFalse(
            Post.objects.filter(
                text='Созданный в тестовом клиенте пост',
                group=self.post.group.id
            ).exists()
        )
        self.assertRedirects(response, f'{reverse_login}?next=/create/')
        self.assertEqual(post_count, Post.objects.count())

    def test_comment_authorized(self):
        """Проверка: Валидная форма создает комментарий в Comment."""
        comment_count = Comment.objects.count()
        data_create = {
            'text': "Созданный в тестовом клиенте комментарий",
        }
        response = self.authorized_client.post(
            (reverse('posts:add_comment', kwargs={'post_id': self.post.id})),
            data_create,
            follow=True
        )
        created_comment = Comment.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text='Созданный в тестовом клиенте комментарий'
            ).exists()
        )
        self.assertEqual(created_comment.text, data_create['text'])

    def test_comment_anonymous(self):
        """Проверка: Комментировать пост могут
        только авторизованные пользователи
        """
        comment_count = Comment.objects.count()
        data_create = {
            'text': "Созданный в тестовом клиенте комментарий",
        }
        response = self.guest_client.post(
            (reverse('posts:add_comment', kwargs={'post_id': self.post.id})),
            data_create
        )
        reverse_login = reverse('users:login')
        self.assertFalse(
            Comment.objects.filter(
                text='Созданный в тестовом клиенте комментарий'
            ).exists()
        )
        self.assertRedirects(
            response,
            f'{reverse_login}?next=/posts/{self.post.id}/comment/'
        )
        self.assertEqual(Comment.objects.count(), comment_count)
