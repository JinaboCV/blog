from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Writer, Article

from django.forms.widgets import PasswordInput, TextInput

# Create a user 
class CreateWriterForm(UserCreationForm):
    phone = forms.CharField(max_length=36, widget=forms.TextInput(attrs={'class': 'form-control w-100'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-100', 'rows': 4}))
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control w-100'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control w-100'})

    def save(self, commit = True):
        user =  super().save(commit=False)
        if commit:
            user.save()
        writer = Writer(user=user, phone=self.cleaned_data['phone'], bio=self.cleaned_data['bio'])
        writer.save()
        return user

# Login a user 
class LoginWriterForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control w-100'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control w-100'}))


# Create an article
class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'thumbnail', 'content', 'tags']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control w-100'}),
            'title': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'content': forms.Textarea(attrs={'class': 'form-control w-100', 'rows': 25}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control w-100'}),
        }


# Update an article
class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'thumbnail', 'content', 'tags']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control w-100'}),
            'title': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'content': forms.Textarea(attrs={'class': 'form-control w-100', 'rows': 25}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control w-100'}),
        }