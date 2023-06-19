from django.urls import path
from .views import NewsList, NewsPage, NewsSearch, NewsAdd,NewsDelete, NewsUpdate, NewsCreateView
from .views import upgrade_me


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsPage.as_view(), name= 'news_detail'),
    path('search/', NewsSearch.as_view()),
    path('add/', NewsAdd.as_view(), name = 'news_add'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name = 'news_delete'),
    path('<int:pk>/edit', NewsUpdate.as_view(), name='news_edit'),

    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
]