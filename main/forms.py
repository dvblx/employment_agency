from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ['user', 'photo']


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ['user']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['employer_id']


class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        exclude = ['applicant', 'additional_education']
