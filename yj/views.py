from django.shortcuts import render
from django.conf.urls import patterns, include, url


# Create your views here.
# For more information on this file, see
# https://docs.djangoproject.com/en//intro/tutorial03/

def home(request):
    context = {
        'active_nav': 'home',
    }
    return render(request, 'home.html', context)
