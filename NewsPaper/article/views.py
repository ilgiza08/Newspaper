from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Category, Author, User
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


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
    

class NewsAdd(PermissionRequiredMixin, CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    permission_required = ('article.add_post', )

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    end_date = datetime.datetime.now()
    #    start_date = end_date - 1
    #    news_count = len(self.request.user__author.posts.filter(time__range=(start_date, end_date)))
    #    context['more_than_three'] = news_count >= 3
    # #    context['more_than_three'] = len(self.request.user__author.posts.filter(time__range=(start_date, end_date)))
    #    return context
        

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
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
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
            body = '',
            from_email='il.ilgiza@yandex.ru', 
            to=[email,],
        )

        msg.attach_alternative(html, "text/html")
        try:
            msg.send()
        except Exception as e:
            print(e)
        return HttpResponse(f"<h2>Вы подписались на категорию {category}</h2>")
        
        
    return redirect('/news/')


def notify_weekly_draft():
    users=User.objects.all()
    for user in users:
        subscriptions = user.category_set.all()
        print(f'USER SUS-N {subscriptions}')

        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)
        
        for sub in subscriptions:
            new_post_list = []
            new_posts = sub.post_set.filter(time__range=(start_date, end_date))
            new_post_list.append(new_posts)
        
    print(f'NEW POST LIST {new_post_list}')

# notify_weekly_draft()




