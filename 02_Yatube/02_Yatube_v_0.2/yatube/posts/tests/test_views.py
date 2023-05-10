from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group
from yatube.settings import PAGE_VIEW_MULTIPLIER

User = get_user_model()


class ViewsTestCase(TestCase):
    fixtures = [
        'posts.xml',
        'groups.xml',
        'users.xml'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.get(pk=1)
        cls.user = User.objects.get(id=2)
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Проверка: view-функция использует соответствующий шаблон."""

        pages_names_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.post.group.slug}):
            'posts/group_list.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
            'posts/post_detail.html',
            reverse('posts:profile', kwargs={'username': self.post.author}):
            'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
            'posts/create_post.html'
        }

        for reverse_name, template in pages_names_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_show_correct_context(self):
        """Проверка: в контекст страниц передаются списки постов"""
        responses = (
            reverse('posts:index'),
            reverse(
                'posts:group_list', kwargs={'slug': self.post.group.slug}
            ),
            reverse(
                'posts:profile', kwargs={'username': self.post.author}
            )
        )
        for reverse_name in responses:
            with self.subTest(path=reverse_name):
                response = self.authorized_client.get(reverse_name)
                for post in response.context['page_obj']:
                    self.assertIsInstance(post, Post)

                single_post = response.context['page_obj'][0]

                self.assertEqual(single_post.text, self.post.text)
                self.assertEqual(single_post.author, self.post.author)
                self.assertEqual(single_post.group, self.post.group)

    def test_profile_post_detail_context_count_posts_correct(self):
        """Проверка: количество постов в контекстах страниц профайла и
        поста корректно
        """
        reverse_names = (
            reverse(
                'posts:profile', kwargs={'username': self.post.author}
            ),
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}
            ),
        )
        for reverse_name in reverse_names:
            with self.subTest(path=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(
                    response.context['count_posts'],
                    self.post.author.posts.count()
                )

    def test_group__list__correct_filter(self):
        """Проверка: на страницу группы выводится список постов,
        отфильтрованных по группе
        """
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.post.group.slug})
        )
        for post in response.context['page_obj']:
            self.assertEqual(post.group, self.post.group)

    def test_profile_correct_filter(self):
        """Проверка: на страницу автора выводится список постов,
        отфильтрованных по автору
        """
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        for post in response.context['page_obj']:
            self.assertEqual(post.author, self.post.author)

    def test_post_detail_correct_filter(self):
        """Проверка: на страницу поста выводится один пост,
        отфильтрованный по id
        """
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(
            response.context['post'].id, self.post.id
        )

    def test_post_create_and_edit_form_fields_correct(self):
        """Проверка: поля форм создания и редактирования поста корректны"""
        reverse_names = (
            reverse('posts:post_create'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for reverse_name in reverse_names:
            response = self.authorized_client.get(reverse_name)
            for field, expected in form_fields.items():
                with self.subTest(field=field):
                    form_field = response.context.get('form').fields.get(field)
                    self.assertIsInstance(form_field, expected)

    def test_post_create_test(self):
        """Проверка: созданный пост появляется на нужных страницах"""
        reverse_names = (
            reverse('posts:index'),
            reverse(
                'posts:group_list', kwargs={'slug': self.post.group.slug}
            ),
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        for reverse_name in reverse_names:
            response = self.authorized_client.get(reverse_name)
            with self.subTest(path=reverse_name):
                self.assertEqual(response.context['page_obj'][0], self.post)

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
            data_edit
        )
        edited_post = Post.objects.first()
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': edited_post.id})
        )

    def test_paginator_first_pages_contains_ten_records(self):
        """Проверка: количество постов на первых страницах
        в соответствии с PAGE_VIEW_MULTIPLIER
        """
        reverse_names = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={
                'slug': self.post.group.slug
            }),
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        for reverse_name in reverse_names:
            response = self.authorized_client.get(reverse_name)
            with self.subTest(path=reverse_name):
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
