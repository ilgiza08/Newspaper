from django.urls import path
from .views import NewsList, NewsPage

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsPage.as_view()),
]