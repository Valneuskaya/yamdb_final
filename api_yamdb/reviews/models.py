import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        "Название категории", max_length=200)
    slug = models.SlugField(
        "slug", unique=True)

    class Meta:
        verbose_name = "Категория"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        "Название жанра", max_length=200)
    slug = models.SlugField(
        "slug", unique=True)

    class Meta:
        verbose_name = "Жанр"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        "Название произведения",
        max_length=256, db_index=True)
    year = models.IntegerField(
        "Год выпуска",
        blank=True,
        validators=[
            MaxValueValidator(
                dt.datetime.now().year,
                message='Год выпуска не может быть позже текущего года'
            )
        ]
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Название категории",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Название жанра",
        blank=True,
        db_index=True,
        related_name='titles',
    )
    description = models.CharField(
        "Описание произведения",
        max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = "Произведение",
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    SCORE = zip(range(1, 11), range(1, 11))
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField("Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор произведения'
    )
    score = models.IntegerField(
        "Оценка", choices=SCORE, default=1)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

    class Meta:
        verbose_name = "Отзыв",
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review"
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField("Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

    class Meta:
        verbose_name = "Комментарий"
