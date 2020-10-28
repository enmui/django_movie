from django.db import models
from datetime import date
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    """Категории."""

    # TODO: Define fields here
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        """Описание метакласса Категории."""

        verbose_name = 'Категория'  # ! Имя модели в ед.ч.
        verbose_name_plural = 'Категории'  # ! Имя модели в мн.ч.

    def __str__(self):
        """Строковое представление Категории."""
        return self.name


class Actor(models.Model):
    """Актеры и режиссеры."""

    # TODO: Define fields here
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    class Meta:
        """Описание метакласса Актеры и режиссеры."""

        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'

    def __str__(self):
        """Строковое представление Актеры и режиссеры."""
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})


class Genre(models.Model):
    """Жанры."""

    # TODO: Define fields here
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        """Описание метакласса Жанры."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Строкове представление Жанров."""
        return self.name


class Movie(models.Model):
    """Фильмы."""

    # TODO: Define fields here
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2020)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(
        Actor, verbose_name="Режиссеры", related_name="film_director"
    )
    actors = models.ManyToManyField(
        Actor, verbose_name="Актеры", related_name="film_actor"
    )
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField(
        "Бюджет", default=0, help_text="указывать сумму в долларах"
    )
    feez_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    feez_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL,
        null=True
    )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        """Описание метакласса Фильмы."""

        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        """Строковое представление Фильмы."""
        return self.title


class MovieShots(models.Model):
    """Кадры из фильма."""

    # TODO: Define fields here
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(
        Movie, verbose_name="Фильм", on_delete=models.CASCADE
    )

    class Meta:
        """Описание метакласса Кадры из фильма."""

        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'

    def __str__(self):
        """Строковое представление Кадры из фильма."""
        return self.title


class RatingStar(models.Model):
    """Звезда рейтинга."""

    # TODO: Define fields here
    value = models.PositiveSmallIntegerField("Значение", default=0)

    class Meta:
        """Описание метакласса Звезда рейтинга."""

        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'

    def __str__(self):
        """Строковое представление Звезда рейтинга."""
        return self.value


class Rating(models.Model):
    """Рейтинг."""

    # TODO: Define fields here
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(
        RatingStar, verbose_name="Звезда", on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie, verbose_name="Фильм", on_delete=models.CASCADE
    )

    class Meta:
        """Описание метакласса Рейтинг."""

        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        """Строковое преставление Рейтинг."""
        return f"{self.star} - {self.movie}"


class Reviews(models.Model):
    """Отзывы."""

    # TODO: Define fields here
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL,
        blank=True, null=True
    )
    movie = models.ForeignKey(
        Movie, verbose_name="Фильм", on_delete=models.CASCADE
    )

    class Meta:
        """Описание метакласса Отзывы."""

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        """Строковое представление Отзывы."""
        return f"{self.name} - {self.movie}"
