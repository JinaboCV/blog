from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Category, Article, Writer, Tag, Subscriber
from django.contrib.auth.models import auth
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateWriterForm, LoginWriterForm, CreateArticleForm, UpdateArticleForm
from django.db.models import Q
from django.contrib import messages

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

# Category Page
def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
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
    query = request.GET.get('query', '').strip()
    if query:
        results = Article.objects.filter(
            Q(category__title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-updated_at').distinct()
    else:
        results = Article.objects.none()

    paginator = Paginator(results, 10)
    page_number = request.GET.get("page")
    article_obj = paginator.get_page(page_number)
    context = {"results": article_obj, "query": query}
    return render(request, 'blogs/search.html', context=context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    recent_articles =  Article.objects.order_by('-updated_at')[:12]
    related_articles = Article.objects.filter(Q(category=article.category) | Q(tags__in=article.tags.all())).exclude(slug=article.slug).distinct()[:8]
    context = {"article" : article, "recent_articles": recent_articles, "related_articles": related_articles}
    return render(request, 'blogs/article-detail.html', context=context)

# Writer Signup 
def writer_signup(request):
    form = CreateWriterForm()
    if request.method == 'POST':
        form = CreateWriterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form, 'hide_navbar': True, 'hide_footer': True}
    return render(request, 'blogs/signup.html', context=context)


# Login a writer
def writer_login(request):
    form = LoginWriterForm()
    if request.method == 'POST':
        form = LoginWriterForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('writer-dashboard')
    context = {'form': form, 'hide_navbar': True, 'hide_footer': True}
    return render(request, 'blogs/login.html', context=context)

# Logout
def writer_logout(request):
    auth.logout(request)
    return redirect('home')

# writer's dashboard
@login_required(login_url='login')
def writer_dashboard(request):
    writer = Writer.objects.get(user=request.user)
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        articles = Article.objects.filter(
            author=writer
        ).filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct().order_by('-updated_at')
    else:
        articles = Article.objects.filter(author=writer).order_by('-updated_at')
    
    context = {
        'articles': articles,
        'search_query': search_query,
        'hide_navbar': True,
        'hide_footer': True
    }
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
def update_article(request, slug):
    article = Article.objects.get(slug=slug)
    form = UpdateArticleForm(instance=article)
    if request.method == 'POST':
        form = UpdateArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')
    context = {'form':form}
    return render(request, 'blogs/update-article.html', context=context)

# Delete an article
@login_required(login_url='login')
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user.writer)
    article.delete()
    return redirect('writer-dashboard')

def terms(request):
    return render(request, 'blogs/terms.html')

def privacy(request):
    return render(request, 'blogs/privacy.html')

def about(request):
    return render(request, 'blogs/about.html')


# Subscribe to the newsletter
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if the email is already subscribed
            if Subscriber.objects.filter(email=email).exists():
                messages.warning(request, "You are already subscribed.")
            else:
                Subscriber.objects.create(email=email)
                messages.success(request, "You have successfully subscribed!")
        else:
            messages.error(request, "Please enter a valid email address.")

    return redirect('home')

