from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from django.shortcuts import render

from .models import Article, Category, Comment
from .forms import CommentForm, SearchForm
from django.db.models import Count
import locale

locale.setlocale(locale.LC_TIME, '')
import time


# Create your views here.

def index(request):
    categories = Category.objects.all()
    last_articles = Article.objects.all().order_by('date')[:5]
    popular_articles = Article.objects.all().annotate(num_comments=Count('comment')).order_by('-num_comments')[:5]
    posts_per_categories = []

    for category in categories:
        posts_per_categories.append([category.title, Article.objects.filter(category=category).order_by('-date')[:5]])

    articles = Article.objects.all()
    context = {
        'categories': categories,
        'last_articles': last_articles,
        'posts_per_categories': posts_per_categories,
        'time': time.strftime('%A %d/%m/%Y'),
        'popular_articles': popular_articles

    }
    return render(request, 'index.html', context)


def article(request, article):
    try:
        categories = Category.objects.all()
        last_articles = Article.objects.all().order_by('date')[:5]
        popular_articles = Article.objects.all().annotate(num_comments=Count('comment')).order_by('num_comments')[:5]
        article = Article.objects.get(pk=article)
        comments = Comment.objects.filter(article=article)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                visitor_name = form.cleaned_data['visitor_name']
                visitor_email = form.cleaned_data['visitor_email']
                content = form.cleaned_data['content']
                comment = Comment(article=article, visitor_name=visitor_name, commenter_email=visitor_email,
                                  content=content)
                comment.save()
                return HttpResponseRedirect(request.path_info)

        else:
            form = CommentForm()
            context = {
                'article': article,
                'form': form,
                'comments': comments,
                'categories': categories,
                'last_articles': last_articles,
                'popular_articles': popular_articles
            }
            return render(request, 'article.html', context)

    except Article.DoesNotExist:
        raise Http404


def articles(request, category):
    categories = Category.objects.all()
    last_articles = Article.objects.all().order_by('date')[:5]
    popular_articles = Article.objects.all().annotate(num_comments=Count('comment')).order_by('num_comments')[:5]
    articles = Article.objects.filter(category=category)
    context = {
        'category': category,
        'articles': articles,
        'categories': categories,
        'last_articles': last_articles,
        'popular_articles': popular_articles
    }
    return render(request, 'articles.html', context)


def search(request):
    categories = Category.objects.all()
    last_articles = Article.objects.all().order_by('date')[:5]
    popular_articles = Article.objects.all().annotate(num_comments=Count('comment')).order_by('num_comments')[:5]
    keywords = ''

    if request.method == 'POST':

        form = SearchForm(request.POST)
        if form.is_valid():
            all_queries = None
            keywords = form.cleaned_data['keywords']
            search_fields = ('title', 'content', 'resume')
            for keyword in keywords.split(' '):
                keyword_query = None
                for field in search_fields:
                    each_query = Q(**{field + 'contains': keyword})
                    if not keyword_query:
                        keyword_query = each_query
                    else:
                        keyword_query = keyword_query | each_query
                        if not all_queries:
                            all_queries = keyword_query
                        else:
                            all_queries = all_queries & keyword_query

            articles = Article.objects.filter(all_queries).distinct()
            context = {
                'keywords': keywords,
                'articles': articles,
                'categories': categories,
                'last_articles': last_articles,
                'popular_articles': popular_articles
            }
            return render(request, 'search.html', context)
