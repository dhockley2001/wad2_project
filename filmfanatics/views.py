from django.shortcuts import render
from filmfanatics.models import Genre, Film, Account, Review
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):

    genre_list = Genre.objects.order_by('name')

    context_dict = {}
    context_dict['genres'] = genre_list

    response = render(request, reverse('filmfanatics:home') , context=context_dict)
    return response

def contact_us(request):

    context_dict = {}

    return render(request, reverse('filmfanatics:contact_us'), context=context_dict)

def show_genre(request, genre_name_slug):

    context_dict = {}

    try:
        genre = Genre.objects.get(slug=genre_name_slug)
        films = Film.objects.filter(genre=genre)

        context_dict['genre'] = genre
        context_dict['films'] = films

    except Genre.DoesNotExist:

        context_dict['category'] = None
        context_dict['films'] = None

    return render(request, reverse('filmfanatics:genre'), context=context_dict)

@login_required
def account(request):

    context_dict = {}

    account = Account.objects.get(user=request.user)

    saved_films = account.saved_films.all()
    created_reviews = Review.objects.filter(account=account)

    context_dict['saved_films'] = saved_films
    context_dict['created_reviews'] = created_reviews

    return render(request, reverse('filmfanatics:account'), context=context_dict)


