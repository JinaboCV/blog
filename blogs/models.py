from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Writer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    author = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True, blank= True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank= True)
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    deleted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


