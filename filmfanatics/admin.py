from django.contrib import admin
from filmfanatics.models import Genre, Film, Account, Review

admin.site.register(Genre)
admin.site.register(Account)
admin.site.register(Film)
admin.site.register(Review)
