from django.urls import path
from .views import (
    MoviesView, MovieDetailView, AddReview, ActorView, FilterMoviesView,
    JsonFilterMoviesView
)


urlpatterns = [
    path("", MoviesView.as_view()),
    path("filter/", FilterMoviesView.as_view(), name="filter"),  # ! Находится
    # ! здесь, чтобы данный url не попадал под обработку поиска url по <slug>
    path("json-filter/", JsonFilterMoviesView.as_view(), name="json_filter"),
    path("<slug:slug>/", MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", ActorView.as_view(), name="actor_detail")
]
