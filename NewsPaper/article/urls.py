from django.urls import path
from .views import NewsList, NewsPage, NewsSearch, NewsAdd,NewsDelete, NewsUpdate, NewsByCategory
from .views import upgrade_me, subscribe
from .views import CategoryList
from django.views.decorators.cache import cache_page



urlpatterns = [
    path('', cache_page(60)(NewsList.as_view())),
    path('<int:pk>', NewsPage.as_view(), name= 'news_detail'),
    path('search/', NewsSearch.as_view()),
    path('add/', NewsAdd.as_view(), name = 'news_add'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name = 'news_delete'),
    path('<int:pk>/edit', NewsUpdate.as_view(), name='news_edit'),

    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('categories/', CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>', NewsByCategory.as_view(), name='news_category'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
]