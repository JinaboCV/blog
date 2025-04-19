from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Article, Writer, Tag


def index(request):
    recent_articles =  Article.objects.order_by('-updated_at')[:12]
    context = {
        'recent_articles':recent_articles
    }
    return render(request, 'blogs/index.html', context=context)




def category_page(request, category_id):
    category = Category.objects.get(id=category_id)
    articles = Article.objects.filter(category=category)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'blogs/category-page.html', context=context)

def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {"article" : article}
    return render(request, 'blogs/article-detail.html', context=context)
