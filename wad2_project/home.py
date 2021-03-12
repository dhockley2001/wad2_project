## home page of the website

from django.shortcuts import render
from django.http import HttpResponse

def(index)(request):
    return HttpResponse ("This the main page")