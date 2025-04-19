from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("article/<int:article_id>", views.article_detail, name="article" ),
    path("category/<int:category_id>", views.category_page, name="category")
]
