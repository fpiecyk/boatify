from django import forms
from django.forms import widgets
from .models import Pier, Boat, Bookings, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class PierForm(forms.ModelForm):
    class Meta:
        model = Pier
        fields = "__all__"
        labels = {
            "name": "Nazwa",
            "address": "Adres"
        }


class BoatForm(forms.ModelForm):
    class Meta:
        model = Boat
        exclude = ('is_available',)
        labels = {
            "pier_id": "Przystań",
            "type": "Typ łodzi",
            "name": "Nazwa łodzi",
            "length": "Długość łodzi",
            "capacity": "Liczba osób",
            "engine_power": "Moc silnika",
            "description": "Opis",
            "image": "Zdjęcie",
            "daily_price": "Cena wynajmu"
        }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Imię')
    last_name = forms.CharField(max_length=30, label='Nazwisko')
    email = forms.EmailField(label='Adres email')
    phone = forms.CharField(max_length=12, label='Telefon komórkowy')
    username = forms.CharField(label='Nazwa użytkownika', min_length=5, max_length=150)
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput)
    wallet = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'username', 'password1', 'password2')
        labels = {
            "username": "Nazwa użytkownika",
            "email": "Adres email",
            "phone": "Telefon komórkowy",
            "password1": "Hasło",
            "password2": "Potwierdź hasło",
            "first_name": "Imię",
            "last_name": "Nazwisko"
        }
        

class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        exclude = ('total_price',)


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        labels = {
            "username": "Nazwa użytkownika",
            "password": "Hasło"
        }


