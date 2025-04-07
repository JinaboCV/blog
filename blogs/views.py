from django.shortcuts import render
from django.http import HttpResponse


def blogger(request):
    return HttpResponse('Hello Blogger')
