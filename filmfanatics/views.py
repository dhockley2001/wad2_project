from filmfanatics.forms import ReviewForm, UserForm, AccountForm
from filmfanatics.models import Genre, Film, Account, Review
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone, date
import random
import json


def home(request):

    genre_list = Genre.objects.order_by('name')

    # find the five most recently released films
    recently_released = Film.objects.order_by('-release')[:5]

    context_dict = {}
    context_dict['genres'] = genre_list
    context_dict['recently_released'] = recently_released


    response = render(request, 'filmfanatics/home.html' , context=context_dict)
    return response

def contact_us(request):

    context_dict = {}

    return render(request, 'filmfanatics/contact_us.html', context=context_dict)

def show_genre(request, genre_name_slug):

    context_dict = {}

    try:
        genre = Genre.objects.get(slug=genre_name_slug)

        # get associated films of the genre
        films = Film.objects.filter(genre=genre)

        context_dict['genre'] = genre
        context_dict['films'] = films

    except Genre.DoesNotExist:

        context_dict['genre'] = None
        context_dict['films'] = None

    return render(request, 'filmfanatics/genre.html', context=context_dict)

def sign_up(request):

    registered = False

    # if submitting the data
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)

        # if both forms are valid save the information
        if user_form.is_valid() and account_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            account = account_form.save(commit=False)
            account.user = user

            # get the profile pciture
            if 'picture' in request.FILES:
                account.picture = request.FILES['picture']

            account.save()

            registered = True

        else:
            # form invalid
            print(user_form.errors, account_form.errors)

    else:
        # render the form
        user_form = UserForm()
        account_form = AccountForm()

    return render(request,
                    'filmfanatics/sign_up.html',
                    context = {'user_form': user_form,
                                'account_form': account_form,
                                'registered': registered})

@login_required
def account(request):

    context_dict = {}

    # get the associated account of the logged in user
    account = Account.objects.get(user=request.user)

    # get the accounts saved films
    saved_films = account.saved_films.all()


    context_dict['saved_films'] = saved_films


    return render(request, 'filmfanatics/account.html', context=context_dict)

@login_required
def write_review(request, film_name_slug=None):

    # check film is valid
    try:
        film = Film.objects.get(slug=film_name_slug)
    except Film.DoesNotExist:
        film = None

    if film is None:
        redirect(reverse('filmfanatics:home'))


    form = ReviewForm()

    # if submitting the review
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if film:
                # save the review information
                review = form.save(commit=False)
                review.posted_at = datetime.now()
                review.film = film
                user = request.user
                account = Account.objects.get(user=user)
                review.account = account
                review.save()
                genre = film.genre

            return redirect(reverse('filmfanatics:genre', kwargs={'genre_name_slug': genre.slug}))

        else:
            print(form.errors)

    return render(request, 'filmfanatics/write_review.html', context={'form': form, 'film': film})

def user_login(request):

    # if submitting the information
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # check user is authenticated and their account is active
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('filmfanatics:home'))
            else:
                return HttpResponse("Your FilmFanatics account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'filmfanatics/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('filmfanatics:home'))

def trending(request):

    # get 10 most viewed films in last 24hrs
    trending_films = Film.objects.order_by('-views')[:10]

    return render(request, 'filmfanatics/trending.html', context={'trending_films': trending_films})

def search(request):

    query = request.GET.get('search')

    # filter films based on search query
    if query:
        films = Film.objects.filter(Q(title__icontains=query))

    return render(request, 'filmfanatics/search.html', {'search_query': query, 'searched_films':films})


def get_random_film(request):

    # check if correct request
    if request.is_ajax and request.method == "GET":

        films = Film.objects.all()

        # get random film
        film = random.choice(films)

        # check if the view counter needs reset
        check_reset(film)

        # increment view counter
        film.views += 1
        film.save()

        # prepare film and review data for response
        response_data = {}

        response_data['title'] = film.title
        response_data['director'] = film.director
        response_data['cast'] = film.cast
        response_data['picture'] = str(film.picture)
        response_data['synopsis'] = film.synopsis
        response_data['views'] = film.views
        response_data['review_number'] = film.review_number
        response_data['average_rating'] = film.average_rating
        response_data['slug'] = film.slug

        # get associated reviews, ordered by revently posted and store them in a list
        getReviews = Review.objects.filter(film=film).order_by('posted_at')

        # store review information in a list
        reviews = [ review.as_dict() for review in getReviews ]

        response_data['reviews'] = reviews

        return HttpResponse(json.dumps(response_data, default=json_serial), content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"error": "Could not get film"}),
            content_type="application/json"
        )

@csrf_exempt
def get_film(request):

    # check if correct request
    if request.is_ajax and request.method == "POST":

        response_data = {}

        # get corresponding film
        filmName = request.POST.get('film')
        film = Film.objects.get(title=filmName)

        # check if the view counter needs reset
        check_reset(film)

        #increment the view counter
        film.views += 1
        film.save()

        # prepare data for response
        response_data['title'] = film.title
        response_data['director'] = film.director
        response_data['cast'] = film.cast
        response_data['picture'] = str(film.picture)
        response_data['synopsis'] = film.synopsis
        response_data['views'] = film.views
        response_data['review_number'] = film.review_number
        response_data['average_rating'] = film.average_rating
        response_data['slug'] = film.slug

        # get reviews ordered by recently posted
        getReviews = Review.objects.filter(film=film).order_by('posted_at')

        # store review information in a list
        reviews = [ review.as_dict() for review in getReviews ]

        response_data['reviews'] = reviews

        return HttpResponse(json.dumps(response_data, default=json_serial), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Could not get film"}),content_type="application/json")

@login_required
@csrf_exempt
def check_film(request):

    # check request
    if request.is_ajax and request.method == "POST":

        # required user and film information from request plus their saved films
        account = Account.objects.get(user=request.user)
        filmName = request.POST.get('name')
        film = Film.objects.get(title=filmName)

        saved = account.saved_films.all()

        if film in saved:
            # if the user has the film in their saved films return true to ajax call, otherwise return false
            return HttpResponse(json.dumps({'saved': True, 'slug': film.slug}, default=json_serial), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'saved': False, 'slug': film.slug}, default=json_serial), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Could not check film"}),content_type="application/json")

@login_required
def save_film(request, film_name_slug):

    # check given film is valid
    try:
        film = Film.objects.get(slug=film_name_slug)
    except Film.DoesNotExist:
        film = None

    if film is None:
        redirect(reverse('filmfanatics:home'))

    # check request
    if request.method == 'GET':

        # get account
        account = Account.objects.get(user=request.user)

        # check if the film is in the users saved films
        if film in account.saved_films.all():
            # if so, the button has been pressed to remove it, so do so
            account.saved_films.remove(film)
        else:
            # otherwise, save the film
            account.saved_films.add(film)
        account.save()

    genre = film.genre
    return redirect(reverse('filmfanatics:genre', kwargs={'genre_name_slug': genre.slug}))



def check_reset(film):
    # helper function called to check if the view count has been reset in the last 24hrs

    if (datetime.now(timezone.utc) - film.reset_at).days > 0:
        film.views = 0
        film.reset_at = datetime.now()
        film.save()

def json_serial(obj):
    # function to assist with the serialization of datetime objects

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))




