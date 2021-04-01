from django.contrib import admin
from filmfanatics.models import Genre, Film, Account, Review

class GenreAdmin(admin.ModelAdmin):

    list_display = ('name', 'graphic')
    prepopulated_fields = {'slug',('name',)}

admin.site.register(Genre)
admin.site.register(Account)
admin.site.register(Film)
admin.site.register(Review)
