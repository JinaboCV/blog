from django.contrib import admin
from .models import Article, Category, Writer, Tag

admin.site.register(Article)
admin.site.register(Writer)
admin.site.register(Category)
admin.site.register(Tag)