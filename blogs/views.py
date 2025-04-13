from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'blogs/index.html')

def article_detail(request):
    return render(request, 'blogs/article-detail.html')

def category_page(request):
    return render(request, "blogs/category-page.html")