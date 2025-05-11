from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Writer, Article

from django.forms.widgets import PasswordInput, TextInput

# Create a user 
class CreateWriterForm(UserCreationForm):
    phone = forms.CharField(max_length=36)
    bio = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit = True):
        user =  super().save(commit=False)
        if commit:
            user.save()
        writer = Writer(user=user, phone=self.cleaned_data['phone'], bio=self.cleaned_data['bio'])
        writer.save()
        return user

# Update a user 
class LoginWriterForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput)
    password = forms.CharField(widget=PasswordInput)


# Create an article
class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'thumbnail', 'content', 'tags']


# Update an article
class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'thumbnail', 'content', 'tags']