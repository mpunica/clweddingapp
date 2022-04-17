from django import forms
from django.core.validators import EmailValidator, URLValidator, ValidationError
from django.contrib.auth.models import User
from .models import BrideGroom_choice, BrideGroom, Guest, Present, SeatTable, Messages

class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class AddUserForm(UserForm):
    password_1 = forms.CharField(widget=forms.PasswordInput,
                                 help_text="Wpisz dwa razy to samo")
    password_2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        if User.objects.filter(username=self.data['username']).exists():
            self.add_error('username', error='Użytkownik już istnieje w bazie')
        return self.data['username']

    def clean(self):
        if self.data['password_1'] != self.data['password_2']:
            self.add_error(None, error='Hasła nie pasują do siebie')
        return super().clean()

    def save(self):
        user_data = self.cleaned_data
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password_1'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
        )
        return user

    class Meta(UserForm.Meta):
        fields = ('username', 'password_1', 'password_2',  "first_name", "last_name", "email")

class ResetPasswordForm(forms.Form):
    password_1 = forms.CharField(widget=forms.PasswordInput,
                                 help_text="Wpisz dwa razy to samo")
    password_2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        if self.data['password_1'] != self.data['password_2']:
            raise ValidationError('Hasła nie pasują do siebie')
        return super().clean()

class AddGuestForm(forms.Form):
    first_name = forms.CharField(label="Imię gościa", max_length=64)
    last_name = forms.CharField(label="Nazwisko gościa", max_length=64)
    is_child = forms.BooleanField(required=False, label="Dziecko")
    bridegrooms = forms.ChoiceField(choices=BrideGroom_choice)
    in_confirmed = forms.BooleanField(required=True, label="Swiętuję razem z Parą Młodą")