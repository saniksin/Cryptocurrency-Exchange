from django.urls import path
from apps.users import views
from django.contrib.auth import views as auth_views
from apps.users.forms import MyPasswordResetForm, CustomSetPasswordForm


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path("logout/", views.user_logout, name="logout"),
    path('register/', views.register, name='register'),
    
    # Смена пароля 
    path('password-change/',
          views.MyPasswordChangeView.as_view(),
          name='change_password'),
    path('password-change/done/',
          views.MyPasswordChangeDoneView.as_view(),
          name='password_change_done'),
        
    #Сброс пароля 
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            form_class=MyPasswordResetForm,
        ),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            form_class=CustomSetPasswordForm
        ),
        name='password_reset_confirm'),
    path('password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]