from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Article, Writer, Tag


def index(request):
    return render(request, 'blogs/index.html')




def category_page(request, category_id):
    category = Category.objects.get(id=category_id)
    articles = Article.objects.filter(category=category)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'blogs/category-page.html', context=context)

def article_detail(request,):
    return render(request, 'blogs/article-detail.html')
