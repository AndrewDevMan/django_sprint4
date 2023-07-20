from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from blogicum.settings import LIMIT_CHARS

User = get_user_model()


class DefaultVerboseNameMadel(models.Model):
    '''Set related name'''
    class Meta:
        abstract = True
        default_related_name = '%(class)ss'


class PublishedModel(models.Model):
    """Абстрактная модель. Добвляет флаг и дату создания."""
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class TitleModel(PublishedModel):
    """Абстрактная модель. Добавляет заголовок."""
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256,
    )

    class Meta:
        abstract = True


class Location(PublishedModel):
    name = models.CharField(
        verbose_name='Название места',
        max_length=256
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(TitleModel):
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(TitleModel):
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'),
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='posts_images',
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta(DefaultVerboseNameMadel.Meta):
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Коментрий'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )

    class Meta(DefaultVerboseNameMadel.Meta):
        verbose_name = 'коментрий'
        verbose_name_plural = 'Коментрии'
        ordering = ('created_at',)

    def __str__(self):
        return (f'Коментарий "{self.author}" к посту "{self.post}": '
                f'"{self.text[:LIMIT_CHARS]}"')
