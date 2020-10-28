from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.
from .models import Movie


class MoviesView(View):
    """Список фильмов"""

    def get(self, request):
        # ! request - это вся информация, присланная от клиента/браузера
        movies = Movie.objects.all()  # ! objects - менеджер по-умолчанию
        return render(
            request, "movies/movies.html", {"movies_list": movies}
        )  # ! возвращаем Http ответ, в который передаем запрос, ссылку на шаблон HTML
        # ! и context - словарь, в кот-м ключ movie_list и значение - это наш список
        # ! записей фильмов


class MovieDetailView(View):
    """Полное описание фильмов"""

    def get(self, request, slug):  # ! pk - это число, передающееся из URL
        movie = Movie.objects.get(url=slug)
        return render(request, "movies/movie_detail.html", {"movie": movie})
