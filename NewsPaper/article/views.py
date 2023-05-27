from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import NewsFilter

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time')
    paginate_by = 10

class NewsPage(DetailView):
    model = Post
    template_name = 'news_page.html'
    context_object_name = 'news_page'

class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) 
        return context



