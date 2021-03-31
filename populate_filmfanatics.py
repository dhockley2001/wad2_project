import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad2_project.settings')

import django
django.setup()
from filmfanatics.models import Genre, Film, Review, Account
from django.contrib.auth.models import User

def populate():

    accounts = [
        {'username': 'johnsmith22',
        'password' : 'dogs2',
        'picture': '/media/profile_images/johnprof.jpg'},
        {'username': 'sallyjohnston123',
        'password' : 'password',
        'picture': '/media/profile_images/sallyprof.jpg'},
        {'username': 'alicesparrow12',
        'password' : 'starwars3',
        'picture': '/media/profile_images/aliceprof.png'},
        ]

    reviews = [
        {'account': accounts[0],
        'posted_at' : datetime(2020, 8, 29),
        'comment': 'Terrible film. Would not recommend.',
        'rating': 1},
        {'account': accounts[1],
        'posted_at' : datetime(2021, 1, 23),
        'comment': 'Okay film, not too bad.',
        'rating': 3},
        {'account': accounts[2],
        'posted_at' : datetime(2020, 4, 6),
        'comment': 'One of my favourites!',
        'rating': 5},
        ]

    comedy_films = [
        {'title': 'Step Brothers',
        'director' : 'Adam McKay',
        'cast' : 'Will Ferrell, John C. Reilly',
        'synopsis' : 'Two aimless middle-aged losers still living at home are forced against their will to become roommates when their parents marry.',
        'release' : datetime(2008, 8, 29),
        'picture': '/static/images/stepbrothers.jpg',
        'reviews': reviews},
        {'title': 'Superbad',
        'director' : 'Greg Mottola',
        'cast' : 'Jonah Hill, Michael Cera, Christopher Mintz-Plasse',
        'synopsis' : 'Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.',
        'release' : datetime(2007, 9, 14),
        'picture': '/static/images/superbad.jpg',
        'reviews': reviews},
        {'title': 'Neighbours',
        'director' : 'Nicholas Stoller',
        'cast' : 'Seth Rogen, Zac Efron, Rose Byrne',
        'synopsis' : 'After they are forced to live next to a fraternity house, a couple with a newborn baby do whatever they can to take them down.',
        'release' : datetime(2014, 5, 3),
        'picture': '/static/images/neighbours.jpg',
        'reviews': reviews}]

    horror_films = [
        {'title': 'Us',
        'director' : 'Jordan Peele',
        'cast' : 'Lupita Nyong`o, Winston Duke',
        'synopsis' : 'A family`s serene beach vacation turns to chaos when their dopplegangers appear and begin to terrorize them.',
        'release' : datetime(2019, 3, 20),
        'picture': '/static/images/us.png',
        'reviews': reviews},
        {'title': 'Insidious',
        'director' : 'James Wan',
        'cast' : 'Patrick Wilson, Rose Byrne, Ty Simpkins',
        'synopsis' : 'A family looks to prevent evil spirits from trapping their comatose child in a realm called The Further.',
        'release' : datetime(2011, 4, 29),
        'picture': '/static/images/insidious.jpg',
        'reviews': reviews},
        {'title': 'Hereditary',
        'director' : 'Ari Aster',
        'cast' : 'Alex Wolff, Gabriel Byrne, Toni Collette',
        'synopsis' : 'A grieving family is haunted by tragic and disturbing occurences',
        'release' : datetime(2018, 6, 8),
        'picture': '/static/images/hereditary.png',
        'reviews': reviews}]

    romance_films = [
        {'title': 'Me Before You',
        'director' : 'Thea Sharrock',
        'cast' : 'Sam Claflin, Emilia Clarke',
        'synopsis' : 'A girl in a small town forms an unlikely bond with a recently paralyzed man she is taking care of.',
        'release' : datetime(2016, 6, 3),
        'picture': '/static/images/mebeforeyou.jpg',
        'reviews': reviews},
        {'title': 'About Time',
        'director' : 'Richard Curtis',
        'cast' : 'Domhnall Gleeson, Rachel McAdams',
        'synopsis' : 'At the age of 21, Tim discovers he can travel in time and change his life. He decides to find a girlfriend and make the world a better place.',
        'release' : datetime(2007, 9, 14),
        'picture': '/static/images/about_time.jpg',
        'reviews': reviews},
        {'title': 'Call Me By Your Name',
        'director' : 'Luca Guadagnino',
        'cast' : 'Timothee Chalamet, Armie Hammer',
        'synopsis' : 'In 1980s Italy, romance blossoms between a 17 year old student and the older man hired as his father`s research assistant.',
        'release' : datetime(2017, 1, 22),
        'picture': '/static/images/cmbyn.png',
        'reviews': reviews}]

    genres = {'Comedy' : {'films': comedy_films, 'graphic': 'static/images/comedy.jpg'},
                'Horror': {'films': horror_films, 'graphic': 'static/images/horror.jpg'},
                'Romance': {'films': romance_films, 'graphic': 'static/images/romance.png'}}

    for genre, genre_data in genres.items():
        g = add_genre(genre, genre_data['graphic'])
        for film in genre_data['films']:
            add_film(g, film['title'], film['director'], film['cast'], film['synopsis'], film['release'], film['picture'], film['reviews'])

def add_film(genre, title, director, cast, synopsis, release, picture, reviews):
    film = Film.objects.get_or_create(genre=genre, title=title)[0]
    film.director = director
    film.cast = cast
    film.synopsis = synopsis
    film.release = release
    film.picture = picture
    film.save()
    add_reviews(film, reviews)
    return film

def add_reviews(film, reviews):

    for review in reviews:
        user = User.objects.get_or_create(username = review['account']['username'], password = review['account']['password'])[0]
        user.save()
        account = Account.objects.get_or_create(user=user)[0]
        account.picture = review['account']['picture']
        account.save()
        newReview = Review.objects.get_or_create(film=film, account=account)[0]
        newReview.posted_at = review['posted_at']
        newReview.comment = review['comment']
        newReview.rating = review['rating']
        newReview.save()




def add_genre(name, graphic):
    genre = Genre.objects.get_or_create(name=name)[0]
    genre.graphic = graphic
    genre.save()
    return genre

if __name__ == '__main__':
    print('Starting FilmFanatics population script...')
    populate()



