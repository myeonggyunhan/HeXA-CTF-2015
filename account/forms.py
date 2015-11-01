from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Account

class CreateForm(UserCreationForm):
        username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'required': 'true', 'autofocus': 'true'}))
        email = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'placeholder': 'E-mail (for prize contact)'}))
        password1 = forms.CharField(min_length=6, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))
        password2 = forms.CharField(min_length=6, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password confirm', 'required': 'true'}))

        class Meta:
                model = User
                fields = ('username', 'email', 'password1', 'password2')

        def save(self, commit=True):
                user = super(CreateForm, self).save(commit=False)
                user.save()
                user_profile = Account(user=user, email=self.cleaned_data.get('email'))

                if commit:
                        user_profile.save()

                return user_profile

        def is_valid(self):
                form = super(CreateForm, self).is_valid()
                return form

        def clean_username(self):
                return self.cleaned_data.get('username')


class AuthForm(AuthenticationForm):
        username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'required': 'true', 'autofocus':'true'}))
        password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))

        def is_valid(self):
                form = super(AuthForm, self).is_valid()
                return form

