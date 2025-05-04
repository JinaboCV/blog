from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="home"),
    path("article/<int:article_id>", views.article_detail, name="article" ),
    path("category/<int:category_id>", views.category_page, name="category"),
    path('writer-dashboard/', views.writer_dashboard, name='writer-dashboard'),
    path('signup', views.writer_signup, name='signup'),
    path('login', views.writer_login, name='login'),
    path('create-article', views.create_article, name='create-article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)