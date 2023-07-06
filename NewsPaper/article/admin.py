from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'good_rating', 'time')
    list_filter = ('author', 'rating')
    search_fields = ('title', )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'ratingAuthor')
    search_fields = ('user', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', )
    list_filter = ('categoryName',)
    search_fields = ('categoryName', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentText', 'commentTime')
    list_filter = ('rating', )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
