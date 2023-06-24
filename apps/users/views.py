from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from apps.users.forms import (
    LoginForm, 
    RegistrationForm, 
    PasswordChangeForm,
)
from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash


# Create your views here.
class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username_or_email'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Ваш аккаунт не активен.'})
            else:
                return render(request, 'login.html', {'form': form, 'error': "Такого пользователя не существует или данные неверны."})
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('index')
        else:
            form_errors = user_form.errors
    else:
        user_form = RegistrationForm()
        form_errors = None
    return render(request, 'registers.html', {'registration_form': user_form, 'errors': form_errors})


class MyPasswordChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password_change_form.html'
    success_url = 'done/'

    def form_valid(self, form):
        update_session_auth_hash(self.request, self.request.user)
        return super().form_valid(form)


class MyPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'password_change_done.html'

