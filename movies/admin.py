from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание", widget=CKEditorUploadingWidget()
        )  # ! Поле, отвечающее за описание фильма
    # ! в данное поле будет добавлен виджет и в админке мы увидим редактор

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")  # ! Кортеж полей для отображения в админке
    list_display_links = ("id", "name")  # ! В административной панели при нажатии на эти поля можно перейти к записи


class ReviewInlines(admin.TabularInline):
    """Отзывы на странице фильмы."""
    model = Reviews  # ! Модель, связанные поля которой будут отображаться в каждой записи основной модели
    extra = 1  # ! Кол-во дополнительных полей(пустых полей)
    readonly_fields = ("name", "email")  # ! Поля, запрещенные для редактирования


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1

    readonly_fields = ("get_image",)

    def get_image(self, object):
        return mark_safe(f"<image src='{object.image.url}' width='50' height='60'>")

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("id", "title", "category", "url", "draft", "get_poster")
    list_display_links = ("id", "title", "category")
    list_filter = ("category", "year")  # ! Добавление панели фильтрации по значениям кортежа выбранных полей
    serch_fields = ("title", "category__name")  # ! Добавление панели поиска по значениям выбранных полей
    inlines = [MovieShotsInline, ReviewInlines]  # ! Отображение всех записей, связанных с записью
    save_on_top = True  # ! Меню сохранения записи снизу и сверху
    save_as = True  # ! Кнопка "Сохранить как новый объект" в меню сохранения
    list_editable = ("draft",)  # ! Возможность редактировать поле в списке отображения записей
    actions = ["publish", "unpublish"]  # ! Действия(функции модели, доступные в админке)
    # fields = ("title", "category", "url", "draft", ("actors", "directors", "genres"),)  # ! Совмещает поля каждого кортежа в кортеже в одну строку
    form = MovieAdminForm
    readonly_fields = ("get_poster",)
    fieldsets = (
        (None, {"fields": (("title", "tagline"),)}),  # ! None - название группы, 'fields' - поля в группе
        (None, {"fields": ("description", "poster", "get_poster")}),
        (None, {"fields": (("year", "world_premiere", "country"),)}),
        ("Actors", {"classes": ("collapse",), "fields": (("actors", "directors", "genres", "category"),)}),
        (None, {"fields": (("budget", "feez_in_usa", "feez_in_world"),)}),
        ("Options", {"fields": (("url", "draft"),)}),
    )

    def get_poster(self, object):
        return mark_safe(f"<image src='{object.poster.url}' width='50' height='60'>")

    def unpublish(self, request, queryset):
        "Убрать из публикации"
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        "Опубликовать"
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"  # ! Краткое описание действия(action'а)
    publish.allowed_permissions = ("change",)  # ! Допустимые разрешения. Чтобы применять данное действие
    # ! у пользователя должны быть права на изменение записи

    unpublish.short_description = "Убрать из публикации"
    unpublish.allowed_permissions = ("change",)

    get_poster.short_description = "Изображение"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("id", "name", "parent", "movie")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("id", "name", "description", "url")
    list_display_links = ("id", "name",)
    readonly_fields = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры/режиссеры"""
    list_display = ("id", "name", "age", "get_image")
    list_display_links = ("id", "name",)
    readonly_fields = ("get_image",)

    def get_image(self, object):
        return mark_safe(f"<image src='{object.image.url}' width='50' height='60'>")

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("id", "ip", "star", "movie")
    list_display_links = ("id", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Картинки к фильму"""
    list_display = ("id", "title", "description", "movie", "get_image")
    list_display_links = ("id", "title")
    readonly_fields = ("get_image",)

    def get_image(self, object):
        return mark_safe(f"<image src='{object.image.url}' width='50' height='60'>")

    get_image.short_description = "Изображение"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """Картинки к фильму"""
    list_display = ("id", "value")
    list_display_links = ("id", "value")


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
# Register your models here.
# admin.site.register(Category, CategoryAdmin)  # ! Связываем модель с классом отображения в админке
