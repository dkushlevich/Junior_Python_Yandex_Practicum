import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post
from yatube.settings import PAGE_VIEW_MULTIPLIER

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ViewsTestCase(TestCase):
    fixtures = [
        'posts.xml',
        'groups.xml',
        'users.xml',
        'comments.xml'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.first()
        cls.user = User.objects.first()

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

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            image=uploaded
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            text='Тестовый комментарий',
            author=cls.user
        )
        cls.data = {
            'index': ('posts:index', None, 'posts/index.html', '/'),
            'group_list': (
                'posts:group_list',
                {'slug': cls.group.slug},
                'posts/group_list.html',
                f'/group/{cls.group.slug}/'
            ),
            'post_detail': (
                'posts:post_detail',
                {'post_id': cls.post.id},
                'posts/post_detail.html',
                f'/posts/{cls.post.id}/'
            ),
            'profile': (
                'posts:profile',
                {'username': cls.post.author},
                'posts/profile.html',
                f'/posts/{cls.post.author}/'
            ),
            'post_create': (
                'posts:post_create',
                None,
                'posts/create_post.html',
                '/create/'
            ),
            'post_edit': (
                'posts:post_edit',
                {'post_id': cls.post.id},
                'posts/create_post.html',
                f'/posts/{cls.post.id}/edit/'

            )
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Проверка: view-функция использует соответствующий шаблон."""

        for _, value in self.data.items():
            path, kwargs, template, _ = value
            with self.subTest(reverse_name=path):
                cache.clear()
                response = self.authorized_client.get(
                    reverse(path, kwargs=kwargs)
                )
                self.assertTemplateUsed(response, template)

    def test_pages_show_correct_context(self):
        """Проверка: в контекст страниц передаются списки постов"""
        test_pages = ['index', 'group_list', 'profile', ]

        for name, value in self.data.items():
            cache.clear()
            if name in test_pages:
                path, kwargs, _, _ = value
                with self.subTest(path=path):
                    response = self.authorized_client.get(
                        reverse(path, kwargs=kwargs)
                    )
                    for post in response.context['page_obj']:
                        self.assertIsInstance(post, Post)

                    single_post = response.context['page_obj'][0]

                    self.assertEqual(single_post.text, self.post.text)
                    self.assertEqual(single_post.author, self.post.author)
                    self.assertEqual(single_post.group, self.post.group)
                    self.assertEqual(single_post.image, self.post.image)

    def test_profile_post_detail_context_count_posts_correct(self):
        """Проверка: количество постов в контекстах страниц профайла и
        поста корректно
        """
        test_pages = ['profile', 'post_detail']

        for name, value in self.data.items():
            path, kwargs, _, _ = value
            if name in test_pages:
                with self.subTest(path=path):
                    response = self.authorized_client.get(
                        reverse(path, kwargs=kwargs)
                    )
                    self.assertEqual(
                        response.context['count_posts'],
                        self.post.author.posts.count()
                    )

    def test_group__list__correct_filter(self):
        """Проверка: на страницу группы выводится список постов,
        отфильтрованных по группе
        """
        path, kwargs, _, _ = self.data['group_list']
        response = self.authorized_client.get(
            reverse(path, kwargs=kwargs)
        )
        for post in response.context['page_obj']:
            self.assertEqual(post.group, self.post.group)

    def test_profile_correct_filter(self):
        """Проверка: на страницу автора выводится список постов,
        отфильтрованных по автору
        """
        path, kwargs, _, _ = self.data['profile']
        response = self.authorized_client.get(
            reverse(path, kwargs=kwargs)
        )
        for post in response.context['page_obj']:
            self.assertEqual(post.author, self.post.author)

    def test_post_detail_correct_filter(self):
        """Проверка: на страницу поста выводится один пост,
        отфильтрованный по id
        """
        path, kwargs, _, _ = self.data['post_detail']
        response = self.authorized_client.get(
            reverse(path, kwargs=kwargs)
        )
        self.assertEqual(response.context['post'], self.post)

    def test_post_create_and_edit_form_fields_correct(self):
        """Проверка: поля форм создания и редактирования поста корректны"""
        test_pages = ['post_edit', 'post_create']

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for name, value in self.data.items():
            if name in test_pages:
                path, kwargs, _, _ = value
                response = self.authorized_client.get(
                    reverse(path, kwargs=kwargs)
                )
                for field, expected in form_fields.items():
                    with self.subTest(field=field):
                        form_field = response.context.get('form').fields.get(
                            field
                        )
                        self.assertIsInstance(form_field, expected)

    def test_post_create_test(self):
        """Проверка: созданный пост появляется на нужных страницах"""
        test_pages = ['index', 'group_list', 'profile']

        data_create = {
            'text': "Созданный в тестовом клиенте пост",
            'group': self.post.group.id
        }
        response = self.authorized_client.post(
            (reverse('posts:post_create')), data_create
        )
        created_post = Post.objects.first()

        for name, value in self.data.items():
            cache.clear()
            if name in test_pages:
                path, kwargs, _, _ = value
                response = self.authorized_client.get(
                    reverse(path, kwargs=kwargs)
                )
                with self.subTest(path=path):
                    self.assertEqual(
                        response.context['page_obj'][0], created_post
                    )

    def test_post_create_post_edit_redirects_works_correct(self):
        """Проверка: при создании и изменении поста пользователя перенаправляет
        на нужную страницу
        """
        data_create = {
            'text': "Созданный в тестовом клиенте пост",
            'group': self.post.group.id
        }
        response = self.authorized_client.post(
            (reverse('posts:post_create')), data_create
        )
        created_post = Post.objects.first()
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': created_post.author})
        )

        data_edit = {
            'text': "Измененный в тестовом клиенте пост",
            'group': self.post.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': created_post.id}),
            data_edit, follow=True
        )
        edited_post = Post.objects.first()
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': edited_post.id})
        )

    def test_paginator_first_pages_contains_ten_records(self):
        """Проверка: количество постов на первых страницах
        в соответствии с PAGE_VIEW_MULTIPLIER
        """
        test_pages = ['index', 'group_list', 'profile']

        for name, value in self.data.items():
            if name in test_pages:
                path, kwargs, _, _ = value
                response = self.authorized_client.get(
                    reverse(path, kwargs=kwargs)
                )
                with self.subTest(path=path):
                    self.assertEqual(
                        len(response.context['page_obj']),
                        PAGE_VIEW_MULTIPLIER
                    )

    def test_paginator_last_pages_contains_correct_records(self):
        """"Проверка: количество постов на последних страницах
        при паджинации корректно"""
        reverse_names = {
            reverse('posts:index'): Post.objects.count(),
            reverse(
                'posts:group_list',
                kwargs={'slug': self.post.group.slug}
            ): Post.objects.filter(group=self.post.group).count(),
            reverse(
                'posts:profile', kwargs={'username': self.post.author}
            ): Post.objects.filter(author=self.post.author).count()
        }
        for reverse_name, posts_count in reverse_names.items():
            page_count = posts_count // PAGE_VIEW_MULTIPLIER + 1
            response = self.authorized_client.get(
                f'{reverse_name}?page={page_count}'
            )
            with self.subTest(path=reverse_name):
                self.assertEqual(
                    len(response.context['page_obj']),
                    (posts_count % PAGE_VIEW_MULTIPLIER)
                )

    def test_context_image_correct(self):
        """Проврека: при выводе поста с картинкой нужное изображение
        передаётся в контексте
        """
        test_pages = ['index', 'group_list', 'profile', 'post_detail']

        for name, value in self.data.items():
            cache.clear()
            if name in test_pages:
                path, kwargs, _, _ = value
                with self.subTest(path=path):
                    response = self.authorized_client.get(
                        reverse(path, kwargs=kwargs)
                    )

                    if name == 'post_detail':
                        self.assertEqual(
                            response.context['post'].image, self.post.image
                        )
                    else:
                        single_post = response.context['page_obj'][0]
                        self.assertEqual(
                            single_post.image, self.post.image
                        )

    def test_post_detail_correct_filter(self):
        """Проверка: на страницу поста корректно выводятся
        комментарии к этому посту
        """
        path, kwargs, _, _ = self.data['post_detail']
        response = self.authorized_client.get(
            reverse(path, kwargs=kwargs)
        )
        post = response.context['post']
        self.assertEqual(post.comments.last(), self.comment)


class CacheTestCase(TestCase):
    fixtures = [
        'posts.xml',
        'groups.xml',
        'users.xml',
        'comments.xml'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.first()
        cls.user = User.objects.first()

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.data = {
            'index': ('posts:index', None, 'posts/index.html', '/'),
        }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache_index(self):
        """Проверка: кеширование главной страницы работает корректно"""
        test_pages = ['index']
        for name, value in self.data.items():
            if name in test_pages:
                path, kwargs, _, _ = value
                with self.subTest(path=path):
                    response = self.authorized_client.get(
                        reverse(path, kwargs=kwargs)
                    )

                    post_for_delete = Post.objects.get(
                        id=response.context['page_obj'][0].id
                    )
                    post_for_delete.delete()

                    cache_response = self.authorized_client.get(
                        reverse(path, kwargs=kwargs)
                    )
                    self.assertEqual(response.content, cache_response.content)

                    cache.clear()

                    cache_cleared_response = self.authorized_client.get(
                        reverse(path, kwargs=kwargs)
                    )
                    self.assertNotEqual(
                        response.content,
                        cache_cleared_response.content
                    )


class FollowTests(TestCase):
    fixtures = fixtures = [
        'posts.xml',
        'groups.xml',
        'users.xml',
        'follows.xml'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.first()
        cls.user_follower = User.objects.first()
        cls.user_following = User.objects.last()

        cls.post = Post.objects.create(
            author=cls.user_following,
            text='Тестовый пост автора',
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client_follower = Client()
        self.authorized_client_follower.force_login(self.user_follower)
        self.authorized_client_following = Client()
        self.authorized_client_following.force_login(self.user_following)

    def test_authorized_follow(self):
        """Проверка: авторизованный пользователь может подписываться на других
        пользователей
        """
        count_follow = Follow.objects.count()
        self.authorized_client_follower.get(reverse(
            'posts:profile_follow',
            kwargs={'username': self.user_following}
        ))
        self.assertEqual(Follow.objects.count(), count_follow + 1)

    def test_authorized_unfollow(self):
        """Проверка: авторизованный пользователь может отписываться от других
        пользователей
        """
        count_follow = Follow.objects.count()
        self.authorized_client_follower.get(reverse(
            'posts:profile_follow',
            kwargs={'username': self.user_following}
        ))
        self.authorized_client_follower.get(reverse(
            'posts:profile_unfollow',
            kwargs={'username': self.user_following}
        ))
        self.assertEqual(Follow.objects.count(), count_follow)

    def test_follow_feed(self):
        """Проверка: новая запись пользователя появляется в ленте тех, кто на
        него подписан и не появляется в ленте тех, кто не подписан
        """
        Follow.objects.create(
            user=self.user_follower,
            author=self.user_following
        )
        response = self.authorized_client_follower.get(
            reverse('posts:follow_index')
        )
        # context = response.context.get('page_obj').object_list
        # context2 = response.context['page_obj']
        # self.assertEqual(context, context2)
        # print(context)
        self.assertIn(self.post, response.context.get('page_obj').object_list)
        self.assertEqual(response.context['page_obj'][0], self.post)

        response = self.authorized_client_following.get(
            reverse('posts:follow_index')
        )
        self.assertNotContains(response, 'Тестовый пост автора')
