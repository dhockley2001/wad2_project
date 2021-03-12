from filmfanatics.forms import ReviewForm, UserForm, AccountForm
from filmfanatics.models import Genre, Film, Account, Review
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def home(request):

    genre_list = Genre.objects.order_by('name')

    context_dict = {}
    context_dict['genres'] = genre_list

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

        context_dict['category'] = None
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

    return render(request, 'fimfanatics/account.html', context=context_dict)

@login_required
def write_review(request):

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('filmfanatics:genre'))

        else:
            print(form.errors)

    return render(request, 'filmfanatics/write_review.html', context={'form': form})

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
    return redirect(reverse('filmfanatics: home'))

def trending(request):

    trending_films = Film.objects.order_by('-views')[:10]

    return render(request, 'filmfanatics/trending.html', context={'trending_films': trending_films})













