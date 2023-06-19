from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

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
    

class NewsAdd(CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm

class NewsDelete(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    
class NewsUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'news_add.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    
    
class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')



