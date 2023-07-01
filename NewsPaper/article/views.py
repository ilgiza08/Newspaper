from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Category, Author, User
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse

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
    
    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        text = request.POST['text']
        author = request.POST['author']
        postCategory = request.POST['postCategory']
 
        post = Post(title=title, text=text, author=Author.objects.get(user=author), postCategory=postCategory)
        post.save()

        send_mail( 
             subject=self.request.POST['title'],
             message=f'Здравствуй, username. Новая статья в твоём любимом разделе!', 
             from_email='il.ilgiza@yandex.ru', 
             recipient_list= ['ilgiza.azamatova@gmail.com',]
         )
        
        return super().get(request, *args, **kwargs)



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
    category.subscribers.add(user)
    # return redirect('/news/catigories')
    return HttpResponse(f"<h2>Вы подписались на категорию {category}</h2>")



   




