from django.urls import path
from filmfanatics import views

app_name = 'filmfanatics'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact_us/', views.contact_us, name = 'contact_us'),
    path('genre/<slug:genre_name_slug>/', views.show_genre, name='genre'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('my_account/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),
    path('trending/', views.trending, name='trending'),
]