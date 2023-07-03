from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.exchange.models import Transaction
from apps.users.forms import LoginForm, PasswordChangeForm, RegistrationForm, UserProfileForm


# Вход юзера
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
                    messages.success(request, 'Вы успешно вошли в систему!')
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Ваш аккаунт не активен.'})
            else:
                return render(request, 'login.html', {'form': form, 'error': "Такого пользователя не существует или данные неверны."})
        return render(request, 'login.html', {'form': form})


# Выход юзера
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, 'Вы успешно вышли!')
    return redirect("index")


# Регистрация нового юзера
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


# Смена пароля
class MyPasswordChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password_change_form.html'
    success_url = 'done/'

    def form_valid(self, form):
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)


# Успешная смена пароля
class MyPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'password_change_done.html'


# Профиль
@login_required
def profile(request):
    user = request.user
    completed_transactions = Transaction.objects.filter(Q(user=user) | Q(email=user.email), status='Finish').count()
    context = {
        'completed_transactions': completed_transactions,
    }
    return render(request, 'profile.html', context)


def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста исправьте сначала все ошибки.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile_update.html', {'form': form})

