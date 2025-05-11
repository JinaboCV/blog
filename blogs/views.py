from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Article, Writer, Tag
from django.contrib.auth.models import auth
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateWriterForm, LoginWriterForm, CreateArticleForm, UpdateArticleForm
from django.db.models import Q


def index(request):
    recent_articles =  Article.objects.order_by('-updated_at')[:12]
    # Cameroon 
    c_articles = Article.objects.filter(category__title__iexact='Cameroon').order_by('?')[:3]
    
    # Politics
    p_articles = Article.objects.filter(category__title__iexact='Politics').order_by('?')[:3]
    
    # World 
    w_articles = Article.objects.filter(category__title__iexact='World').order_by('?')[:3]
    
    context = {
        'recent_articles':recent_articles,
        'c_articles': c_articles,
        'p_articles':p_articles,
        'w_articles': w_articles,
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

# Search article
def search(request):
    query = request.GET.get('query', '')
    results = Article.objects.filter(
        Q(category__title__icontains=query) |
        Q(tags__name__icontains=query) |
        Q(title__icontains=query) |
        Q(content__icontains=query)
    ).distinct()

    context = {"results": results, "query": query}
    return render(request, 'blogs/search.html', context=context)

def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    recent_articles =  Article.objects.order_by('-updated_at')[:12]
    related_articles = Article.objects.filter(Q(category=article.category) | Q(tags__in=article.tags.all())).exclude(id=article.id).distinct()[:8]
    context = {"article" : article, "recent_articles": recent_articles, "related_articles": related_articles}
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
        form = CreateArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.writer
            article.save()
            form.save()
            return redirect('writer-dashboard')
    context = {'form':form}
    return render(request, 'blogs/create-article.html', context=context)
    
# Update an article
@login_required(login_url='login')
def update_article(request, article_id):
    article = Article.objects.get(id=article_id)
    form = UpdateArticleForm(instance=article)
    if request.method == 'POST':
        form = UpdateArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')
    context = {'form':form}
    return render(request, 'blogs/update-article.html', context=context)

# Delete an article
@login_required(login_url='login')
def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    article.delete()
    return redirect('writer-dashboard')
