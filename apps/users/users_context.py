from apps.users.forms import LoginForm, RegistrationForm

# Форма логина
def get_login_form(request):
    return {"login_form": LoginForm()}

# Форма регистарции
def get_registration_form(request):
    return {"registration_form": RegistrationForm()}