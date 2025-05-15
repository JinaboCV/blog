from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="home"),
    path("article/<slug:slug>/", views.article_detail, name="article"),
    path("category/<slug:slug>/", views.category_page, name="category"),
    path('writer-dashboard/', views.writer_dashboard, name='writer-dashboard'),
    path('signup/', views.writer_signup, name='signup'),
    path('login/', views.writer_login, name='login'),
    path('logout/', views.writer_logout, name='logout'),
    path('create-article/', views.create_article, name='create-article'),
    path('search/', views.search, name='search'),
    path('update-article/<slug:slug>/', views.update_article, name='update-article'),
    path('delete-article/<slug:slug>/', views.delete_article, name='delete-article'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('about/', views.about, name='about'),
    path('subscribe/', views.subscribe, name='subscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)