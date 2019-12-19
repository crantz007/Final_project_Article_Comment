from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin import AdminSite
from .models import Article, Category, Comment


# Register your models here.

class ArtcileAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date', 'summary')
    list_display_links = ('title', 'category', 'date', 'summary')
    search_fields = ('title', 'content', 'summary')
    list_per_page = 25


class CommentAdmin(ModelAdmin):
    list_display = ('article', 'visitor_name', 'visitor_email', 'date', 'content')
    list_display_links = ('article', 'visitor_name', 'visitor_email', 'date', 'content')
    search_fields = ('title', 'content')
    list_per_page = 25


admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
