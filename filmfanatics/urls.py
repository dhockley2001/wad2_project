from django.urls import path
from filmfanatics import views

app_name = 'filmfanatics'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact_us/', views.contact_us, name = 'contact_us'),
    path('genre/<slug:genre_name_slug>/', views.show_genre, name='genre'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('write_review/', views.write_review, name='write_review1'),
    path('write_review/<slug:film_name_slug>/', views.write_review, name='write_review2'),
    path('my_account/', views.account, name='account'),
    path('logout/', views.user_logout, name='logout'),
    path('trending/', views.trending, name='trending'),
    path('search/', views.search, name="search"),
    path('get/ajax/get_random_film/', views.get_random_film, name = 'get_random_film'),
    path('post/ajax/get_film/', views.get_film, name = 'get_film'),
    path('post/ajax/check_film/', views.check_film, name = 'check_film'),
    path('save_film/', views.save_film, name = 'save_film'),
    path('save_film/<slug:film_name_slug>/', views.save_film, name = 'save_film2'),
]

