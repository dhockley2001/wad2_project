from django import forms
from django_starfield import Stars
from django.contrib.auth.models import User
from filmfanatics.models import Account, Review

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('bio', 'picture',)

class ReviewForm(forms.ModelForm):

    comment = forms.CharField(widget=forms.Textarea, help_text = "Please enter your review of the film.")
    rating = forms.IntegerField(widget=Stars, help_text = "Choose your rating out of 5 stars.")

    class Meta:
        model = Review
        exclude = ('account', 'film', 'posted_at')