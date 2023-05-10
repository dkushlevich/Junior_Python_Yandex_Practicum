from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('Адрес', unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):

    POST_STR_SLICE: int = 20

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='posts')
    image = models.ImageField('Картинка', upload_to='posts/',
                              blank=True, null=True)
    group = models.ForeignKey(Group, verbose_name='Группа',
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              blank=True, null=True,)

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return (f'"{self.text[:self.POST_STR_SLICE]}". '
                f'Группа: "{self.group}". '
                f'Автор: {self.author.get_username()}')


class Comment(models.Model):

    COMMENT_STR_SLICE: int = 15

    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments')
    post = models.ForeignKey(Post, verbose_name='Пост',
                             on_delete=models.CASCADE,
                             related_name='comments')
    text = models.TextField('Текст')
    created = models.DateTimeField('Дата добавления',
                                   auto_now_add=True,
                                   db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return (f'"{self.text[:self.COMMENT_STR_SLICE]}". '
                f'Пост: "{self.post.text[:self.COMMENT_STR_SLICE]}". '
                f'Автор: {self.author.get_username()}.')


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',)
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follower_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("following")),
                name='check_not_self'
            ),
        ]

    def __str__(self) -> str:
        return (f'Подписка {self.user.get_username()} '
                f'на {self.following.get_username()}')
