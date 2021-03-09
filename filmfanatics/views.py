from django.shortcuts import render
from filmfanatics.models import Genre


def home(request):

    genre_list = Genre.objects.order_by('name')

    context_dict = {}
    context_dict['genres'] = genre_list

    response = render(request, 'filmfanatics/home.html', context=context_dict)
    return response
