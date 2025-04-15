from django.contrib import admin
from .models import Article, Category, Writer, Tag

class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'category', 'author')

admin.site.register(Article, AdminArticle)
admin.site.register(Writer)
admin.site.register(Category)
admin.site.register(Tag)