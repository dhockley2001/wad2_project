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
        films = Film.objects.filter(genre=genre)

        context_dict['genre'] = genre
        context_dict['films'] = films

    except Genre.DoesNotExist:

        context_dict['genre'] = None
        context_dict['films'] = None

    return render(request, 'filmfanatics/genre.html', context=context_dict)

def sign_up(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)

        if user_form.is_valid() and account_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            account = account_form.save(commit=False)
            account.user = user

            if 'picture' in request.FILES:
                account.picture = request.FILES['picture']

            account.save()

            registered = True

        else:
            print(user_form.errors, account_form.errors)

    else:
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

    account = Account.objects.get(user=request.user)

    saved_films = account.saved_films.all()
    created_reviews = Review.objects.filter(account=account)

    context_dict['saved_films'] = saved_films
    context_dict['created_reviews'] = created_reviews

    return render(request, 'filmfanatics/account.html', context=context_dict)

@login_required
def write_review(request, film_name_slug=None):

    try:
        film = Film.objects.get(slug=film_name_slug)
    except Film.DoesNotExist:
        film = None

    if film is None:
        redirect(reverse('filmfanatics:home'))


    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if film:
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

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

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

    trending_films = Film.objects.order_by('-views')[:10]

    return render(request, 'filmfanatics/trending.html', context={'trending_films': trending_films})

def search(request):

    query = request.GET.get('search')

    if query:
        films = Film.objects.filter(Q(title__icontains=query))

    return render(request, 'filmfanatics/search.html', {'search_query': query, 'searched_films':films})


def get_random_film(request):
    if request.is_ajax and request.method == "GET":

        films = Film.objects.all()
        film = random.choice(films)
        # check if the view counter needs reset
        check_reset(film)
        film.views += 1
        film.save()


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

        getReviews = Review.objects.filter(film=film).order_by('posted_at')

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

    if request.is_ajax and request.method == "POST":

        response_data = {}

        filmName = request.POST.get('film')
        film = Film.objects.get(title=filmName)
        # check if the view counter needs reset
        check_reset(film)
        film.views += 1
        film.save()


        response_data['title'] = film.title
        response_data['director'] = film.director
        response_data['cast'] = film.cast
        response_data['picture'] = str(film.picture)
        response_data['synopsis'] = film.synopsis
        response_data['views'] = film.views
        response_data['review_number'] = film.review_number
        response_data['average_rating'] = film.average_rating
        response_data['slug'] = film.slug

        getReviews = Review.objects.filter(film=film).order_by('posted_at')

        reviews = [ review.as_dict() for review in getReviews ]

        response_data['reviews'] = reviews

        return HttpResponse(json.dumps(response_data, default=json_serial), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Could not get film"}),content_type="application/json")

@login_required
@csrf_exempt
def check_film(request):
    print("arrived check")
    if request.is_ajax and request.method == "POST":

        account = Account.objects.get(user=request.user)
        filmName = request.POST.get('name')
        film = Film.objects.get(title=filmName)

        saved = account.saved_films.all()
        print(saved.count())

        if film in saved:
            print("film found")
            return HttpResponse(json.dumps({'saved': True, 'slug': film.slug}, default=json_serial), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'saved': False, 'slug': film.slug}, default=json_serial), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Could not check film"}),content_type="application/json")

@login_required
def save_film(request, film_name_slug):
    print("arrived")

    try:
        film = Film.objects.get(slug=film_name_slug)
    except Film.DoesNotExist:
        film = None

    if film is None:
        redirect(reverse('filmfanatics:home'))

    if request.method == 'GET':

        account = Account.objects.get(user=request.user)

        if film in account.saved_films.all():
            print("Film is in saved_films")
            account.saved_films.remove(film)
        else:
            print("adding film")
            account.saved_films.add(film)
        account.save()

    genre = film.genre
    return redirect(reverse('filmfanatics:genre', kwargs={'genre_name_slug': genre.slug}))



def check_reset(film):

    if (datetime.now(timezone.utc) - film.reset_at).days > 0:
        film.views = 0
        film.reset_at = datetime.now()
        film.save()

def json_serial(obj):

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))




