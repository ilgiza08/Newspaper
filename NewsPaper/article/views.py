from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic import DeleteView
from .models import Post, Category, Author
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.conf import settings
from django.core.cache import cache


class NewsList(ListView):
    """Выводит страницу со списком статей"""
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        # context = 1/0
        return context


class NewsPage(DetailView):
    """Выводит страницу отдельной статьи"""
    model = Post
    template_name = 'news_page.html'
    context_object_name = 'news_page'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        
        return obj


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, 
                                       queryset=self.get_queryset()) 
        return context
    

class NewsAdd(PermissionRequiredMixin, CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    permission_required = ('article.add_post', )
        

class NewsDelete(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    permission_required = ('article.change_post', )

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context
    

@login_required
def upgrade_me(request):
    """Добавляет пользователя в список авторов"""
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/news/')


class CategoryList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'category_list'
    queryset = Category.objects.all()


class NewsByCategory(DetailView):
    model = Category
    template_name = 'news_by_category.html'
    context_object_name = 'news_by_category'


@login_required
def subscribe(request, pk):
    """Добавляет пользователя в список подписчиков категории"""
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        print(category.subscribers.all)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'user': user,
                'category': category,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{category}',
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[email, ],
        )

        msg.attach_alternative(html, "text/html")
        try:
            msg.send()
        except Exception as e:
            print(e)
        return HttpResponse(f"<h2>Вы подписались на категорию {category}</h2>")   
    return redirect('/news/')
