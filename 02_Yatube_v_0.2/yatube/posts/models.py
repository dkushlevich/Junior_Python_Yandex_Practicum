from django.contrib.auth import get_user_model
from django.db import models

from yatube.settings import POST_STR_MULTIPLIER

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Имя', max_length=200)
    slug = models.SlugField('Адрес', unique=True)
    description = models.TextField('Описание')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField('Текст поста', help_text='Введите текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='posts', )
    group = models.ForeignKey(Group,
                              verbose_name='Группа',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              help_text=('Группа, к которой '
                                         'будет относиться пост'),)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[:POST_STR_MULTIPLIER]
