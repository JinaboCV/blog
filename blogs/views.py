from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Article, Writer, Tag
from django.contrib.auth.models import auth
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateWriterForm, LoginWriterForm, CreateArticleForm, UpdateArticleForm


def index(request):
    recent_articles =  Article.objects.order_by('-updated_at')[:12]
    context = {
        'recent_articles':recent_articles
    }
    return render(request, 'blogs/index.html', context=context)


def category_page(request, category_id):
    category = Category.objects.get(id=category_id)
    articles = Article.objects.filter(category=category).order_by('-updated_at')

    paginator = Paginator(articles, 5)
    page_number = request.GET.get("page")
    article_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'articles': article_obj
    }
    return render(request, 'blogs/category-page.html', context=context)

def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    recent_articles =  Article.objects.order_by('-updated_at')[:12]
    context = {"article" : article, "recent_articles": recent_articles}
    return render(request, 'blogs/article-detail.html', context=context)

# Writer Signup 
def writer_signup(request):
    form = CreateWriterForm()
    if request.method == 'POST':
        form = CreateWriterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')
    context = {'form': form}
    return render(request, 'blogs/signup.html', context=context)


# Login a writer
def writer_login(request):
    form = LoginWriterForm()
    if request.method == 'POST':
        form = LoginWriterForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('writer-dashboard')
    context = {'form': form}
    return render(request, 'blogs/login.html', context=context)

# Logout
def writer_logout(request):
    auth.logout(request)
    return redirect('login')

# writer's dashboard
@login_required(login_url='login')
def writer_dashboard(request):
    writer = Writer.objects.get(user=request.user)
    articles = Article.objects.filter(author=writer)
    context = {'articles': articles}
    return render(request, 'blogs/writer-dashboard.html', context)
    

# Add an article
@login_required(login_url='login')
def create_article(request):
    form = CreateArticleForm()
    if request.method == 'POST':
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')
    context = {'form':form}
    return render(request, 'blogs/create-article.html', context=context)
    
    