from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        ratPost = Post.objects.filter(author__user = self.user).aggregate(postRating=Sum('rating'))['postRating']
        ratComment = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))['commentRating']
        ratPostComment = Comment.objects.filter(postComment__author__user = self.user).aggregate(postCommentRat=Sum('rating'))['postCommentRat']

        self.ratingAuthor = ratPost * 3 + ratComment + ratPostComment
        self.save() 


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.categoryName}'
    

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_TYPE = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    )
    postType = models.CharField(max_length=2, choices=POST_TYPE, default=ARTICLE)
    time = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return f'/news/{self.id}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating += 1
        self.save()

    def deslike(self):
        self.rating -= 1
        self.save()


    def preview(self):
        text = self.text[:124]
        return text + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    postComment = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentTime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def deslike(self):
        self.rating -= 1
        self.save()

