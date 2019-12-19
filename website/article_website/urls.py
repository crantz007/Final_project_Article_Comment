from django.conf.urls import url
from . import views

urlpatterns = [
    # localhost:8080/
    url(r'^$', views.index, name='index'),
    # /localhost:8080/article/article_id
    url(r'^article/(?P<article>[\w-]+)/', views.article, name='article'),
    url(r'^search/', views.search, name='search'),
    # /localhost:8080/categories/category_name
    url(r'^categories/(?P<category>[\w-]+)/', views.articles, name='articles')
]
