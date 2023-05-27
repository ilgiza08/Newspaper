from django.urls import path
from .views import NewsList, NewsPage, NewsSearch

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsPage.as_view()),
    path('search/', NewsSearch.as_view())
]