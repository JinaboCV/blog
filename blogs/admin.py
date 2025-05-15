from django.contrib import admin
from .models import Article, Category, Writer, Tag, Subscriber

class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'category', 'author')
    search_fields = ('title', 'category', 'author')
    list_filter = ('category', 'author')        

class AdminSubscriber(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)   

class AdminWriter(admin.ModelAdmin):
    list_display = ('user', 'phone', 'bio')
    search_fields = ('user', 'phone', 'bio')
    list_filter = ('user', 'phone', 'bio')

class AdminCategory(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'slug', 'description')
    list_filter = ('title', 'slug', 'description')
    
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')

admin.site.register(Article, AdminArticle)
admin.site.register(Writer, AdminWriter)
admin.site.register(Category, AdminCategory)
admin.site.register(Tag, AdminTag)
admin.site.register(Subscriber, AdminSubscriber)