from apps.users.forms import LoginForm, RegistrationForm

def get_login_form(request):
    return {"login_form": LoginForm()}

def get_registration_form(request):
    return {"registration_form": RegistrationForm()}