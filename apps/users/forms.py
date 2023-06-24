from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm, PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control"}),
        label="Username or Email:"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        label="Пароль"
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
    label='Пароль', 
    widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Повторите пароль', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        validate_password(cd['password2'])
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if not cd['email']:
            raise forms.ValidationError('Это поле обязательно.')
        elif User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('Пользователь с таким Email уже существует.')
        return cd['email']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return cd['username']


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Старый пароль',
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Новый пароль',
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Повторите новый пароль',
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if not check_password(old_password, self.user.password):
            self.add_error('old_password', 'Введен неправильный старый пароль')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.add_error('new_password2', 'Пароли не совпадают')

        try:
            password_validation.validate_password(new_password1, self.user)
        except ValidationError as e:
            self.add_error('new_password1', e)

    def save(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if new_password1:
            self.user.set_password(new_password1)
            self.user.save()


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email адресс',
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )