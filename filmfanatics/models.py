from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime, timezone

class Genre(models.Model):

    NAME_MAX_LENGTH = 30

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    graphic = models.ImageField(upload_to='genre_graphics')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Film(models.Model):

    TITLE_MAX_LENGTH = 50
    DIRECTOR_MAX_LENGTH = 30

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    director = models.CharField(max_length=DIRECTOR_MAX_LENGTH)
    cast = models.TextField()
    picture = models.ImageField(upload_to='film_images')
    synopsis = models.TextField()
    release = models.DateField(null=True)
    views = models.IntegerField(default=0)
    reset_at = models.DateTimeField(default=datetime.now(timezone.utc))
    average_rating = models.PositiveIntegerField(default=3, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Account(models.Model):

    BIO_MAX_LENGTH = 500

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    saved_films = models.ManyToManyField(Film)

    def __str__(self):
        return self.user.username

class Review(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    #update film stats when review is made
    def save(self, *args, **kwargs):
        self.film.review_number = Review.objects.filter(film = self.film).count()
        if self.film.review_number != 0:
            count = 0
            for review in Review.objects.filter(film=self.film):
                count += review.rating
            self.film.average_rating = count // self.film.review_number
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return self.account + " (" + self.posted_at + ")"

    def as_dict(self):
        return {
            "username": self.account.user.username,
            "profile_pic": str(self.account.picture),
            "posted_at": self.posted_at,
            "comment": self.comment,
            "rating": self.rating,
        }





