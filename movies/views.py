from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http.response import JsonResponse

# Create your views here.
from .models import Movie, Category, Actor, Genre
from .forms import ReviewForm


# !Альтернатива методу get_context_data
class GenreYear(object):
    """Жанры и года"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """Список фильмов"""

    model = Movie
    # ! Если не указать queryset, то ListView возьмет model.objects.all
    queryset = Movie.objects.filter(draft=False)
    # queryset = Movie.objects.all()
    # ! Если не указывать явно, то джанго возьмет model + _ + list(ListView)
    template_name = "movies/movie_list.html"


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        # print(request.POST, '\n')
        # ! Проверка валидности данных с помощью формы
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # ! Сохраняем форму, но не передаем изменения
            # ! в БД, для дальнейшего внесения изменений в данные формы
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie  # ! Привязываем отзыв к фильму
            form.save()  # ! Сохраняем изменения, внося их в БД
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)
